from django.shortcuts import render,get_object_or_404,redirect
from Customers.models import User,User_address,Wallet,Transaction
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from Customers.models import Cart,Cart_items
from Customers.views import Checkout,user_profile
from authentication.views import user_login
from django.utils import timezone
from .models import Order,Order_item,Order_cancellation
from adminn.models import Coupon
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings
from django.http import HttpResponseBadRequest
from orders.forms import OrderCancellationForm


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from Product.models import ProductOffer,Category_offer



# Create your views here.

def Order_success(request):
    if 'user' not in request.session:
        return redirect(user_login)
    
    if request.method == "POST":
        username = request.session['user']
        select_address_id = request.POST.get('address')
        payment = request.POST.get('pay-method')
        coupon = request.POST.get('coupon')

        user = get_object_or_404(User, username=username)

        try:
            address = User_address.objects.get(pk=select_address_id)
        except User_address.DoesNotExist:
            return HttpResponse("Error: Address doesn't exist")
        
        try:
            cart = Cart.objects.get(customer_id=user.id)
            cart_items = Cart_items.objects.filter(cart=cart)
        except Cart.DoesNotExist:
            return HttpResponse("Error: Cart not found")

        if not cart_items.exists():
            return HttpResponse("Error: Cart items not found")
        
        total_price = 0
        order_items = []
        

        for item in cart_items: 
            product = item.product
            category_offer = Category_offer.objects.filter(category=item.product.category,
                                                            start_date__lte=timezone.now(),
                                                            end_date__gte=timezone.now()).first()
            
            print(category_offer)
                                
                
            product_offer=ProductOffer.objects.filter(product=item.product,start_date__lte=timezone.now(),end_date__gte=timezone.now()).first()
            
                
            if category_offer is not None:
                category_product_price = Decimal(item.product.price) - (Decimal(item.product.price) * category_offer.discount_percentage / Decimal('100'))
                print((Decimal(item.product.price) * category_offer.discount_percentage / Decimal('100')),'categgory offer of the product')
                print(category_product_price)

            if product_offer is not None:
                product_product_price=Decimal(item.product.price)-Decimal(product_offer.discount_price)
                print(product_product_price)
            
            if category_offer is not None and product_offer is not None:
                print('inside both offers')
                print(category_product_price)
                print(product_product_price)
                if category_product_price > product_product_price:
                    print(product_product_price)
                    product_price = product_product_price
                else:
                    print(category_product_price)
                    product_price = category_product_price
            elif category_offer:
                product_price=category_product_price
            elif product_offer:
                product_price = product_product_price
            else:
                product_price = item.product.price

            if item.quantity > product.stock:
                print('stock limit exceeds')
                
                return redirect(Checkout)
            
            total_price += item.quantity * product_price
            order_items.append((product, item.quantity, product.price))
            print(total_price)
        # total_price=sum( total_price for item in cart_items)
        print(total_price)



        if coupon:
            
            try:
                coupon = Coupon.objects.get(coupon_code=coupon, is_active=True)
                if total_price >= coupon.min_purchase_amount:
                    
                    total_price -= float(coupon.discount)
                    
                else:
                    return HttpResponse("Error: Minimum purchase amount for the coupon is not met")
            except Coupon.DoesNotExist:
                return HttpResponse("Error: Invalid coupon code")
            print('after coupon applied total_price',total_price )
        
            
        
        
        order = Order.objects.create(
            user=user,
            created_at=timezone.now(),
            total_price=total_price,
            status='Pending',
            street_address=address.street,
            city=address.city,
            district=address.district,
            state=address.state,
            pincode=address.pincode,
            payment=payment,
            payment_status='Pending',
            coupon=coupon if coupon else None 
        ) 
    
        for product, quantity, price in order_items:
            Order_item.objects.create(
                order=order,
                Product=product,
                quantity=quantity,
                price=price
            )

            product.stock -= quantity
            product.save()
        
        cart_items.delete()
        if payment == 'razorpay':
            print("haii")
            request.session['total_price'] = str(total_price)
            request.session['order_id'] = order.id
            return redirect(paymenthomepage)
        if payment == 'wallet':
            wallet = get_object_or_404(Wallet,user = user)
            transaction = Transaction.objects.filter(wallet = wallet)
            if wallet.amount > total_price:
                wallet.amount -= total_price
                wallet.save()
                order.payment_status = 'paid'
                order.save()
                
                Transaction.objects.create(wallet=wallet, amount=total_price, transaction_type='debit')
            else:
                return HttpResponse('Error : insufficient fund in wallet')
            
        return render(request, 'order-success.html')
    
    return redirect(Checkout)


def ordercancel(request,pk):
    if 'user' in request.session:
        print('user')
        username = request.session['user']
        user = User.objects.get(username  = username)

        order = Order.objects.get(id = pk)
        orderitem = Order_item.objects.filter(order_id = order.id)

        if request.method == 'POST':
            print('reason post')
            form = OrderCancellationForm(request.POST)

            if form.is_valid():

                for item in orderitem:
                    item.Product.stock +=item.quantity
                    item.Product.save()
        
                order.is_cancelled = True
            
                order.save()
                if order.payment_status == 'paid':
                    wallet = get_object_or_404(Wallet,user = user)
                    transaction = Transaction.objects.filter(wallet = wallet)
                    wallet.amount += order.total_price
                    wallet.save()
                    order.payment_status = 'refunded to your wallet'
                    order.save()

                    Transaction.objects.create(wallet=wallet, amount=order.total_price, transaction_type='credit')

                
                Order_cancellation.objects.create(
                    order=order,
                    reason=form.cleaned_data['reason']
                )

                return redirect(user_profile,pk = user.id)
        else:
            form = OrderCancellationForm()
            return render(request, 'order_cancel.html', {'order': order,'form': form})
        
    return redirect(user_login)





    
def returnrequest(request,pk):
    if 'user' in request.session:
        username = request.session['user']
        user = User.objects.get(username  = username)

        
        order=Order.objects.get(id=pk)
        
        order.is_return=True
        order.return_status = 'Return requested'
        order.save()
        print('return')
        return redirect(user_profile,pk = user.id)
    return redirect(user_login)


razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def paymenthomepage(request):
    total_price=Decimal(request.session.get('total_price'))
    currency='INR'
    amount=float(total_price) * 100
    print(amount)

    razorpay_order = razorpay_client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
    
    razorpay_order_id=razorpay_order['id']
    callback_url = 'paymenthandler/'
    print(razorpay_order_id)

    context={}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    print("yess")

    return render(request, 'payment.html', context=context)



@csrf_exempt
def paymenthandler(request):
    print("hyyy")
    if 'adminn' in request.session:
        print('paymenthandeler')
        
        if request.method =='POST':
            print('inside payment POSt')
            try:
                
                payment_id = request.POST.get('razorpay_payment_id', '')
                razorpay_order_id = request.POST.get('razorpay_order_id', '')
                signature = request.POST.get('razorpay_signature', '')
                params_dict = {
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_payment_id': payment_id,
                    'razorpay_signature': signature
                }
                
                
                result = razorpay_client.utility.verify_payment_signature(
                    params_dict)
                
                if result is not None:
                    total_price=request.session.get('total_price')
                    amount=float(total_price) * 100

                    try:
                        print("success try")
                        # capture the payemt
                        razorpay_client.payment.capture(payment_id, amount)
                        
                        order_id=request.session.get('order_id')
                        print("ordeeeeerrrid",order_id)
                        order=Order.objects.get(id=order_id)
                        order.payment_status='Paid'
                        order.save()
                        
                        session_data = []
                        for key, value in request.session.items():
                            session_data.append(f'{key}: {value}')
                        
                        session_details = '<br>'.join(session_data)
                        
                        print(session_details)
                        
                        del request.session['total_price']
                        del request.session['order_id']

                        return render(request, 'order-success.html')
                    except:
                        
                        print("payment failed")
                        # if there is an error while capturing payment.
                        return render(request, 'paymentfail.html')
                else:
                    print("failed")
                    return render(request, 'paymentfail.html')
            except:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()
    return redirect(user_login)



def order_pdf_view(request,pk):

    print('pdf')

    if 'user' in request.session:
        username = request.session['user']
        user = get_object_or_404(User,username=username)
        order = get_object_or_404(Order,id=pk)
        order_items = Order_item.objects.filter(order_id = order.id)
        total_order_price = sum(item.price for item in order_items)

        template_path = 'orderdetailpdf.html'
        context = {'order':order,'order_items':order_items,'total_order_price':total_order_price,'user':user,'coupon':order.coupon}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
        html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    return redirect(user_login)


