from django.shortcuts import render,get_object_or_404,redirect
from Customers.models import User,User_address,Wallet,Transaction
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from Customers.models import Cart,Cart_items
from Customers.views import Checkout,user_profile
from authentication.views import user_login
from django.utils import timezone
from .models import Order,Order_item,Order_cancellation,return_reason
from adminn.models import Coupon
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings
from django.http import HttpResponseBadRequest,JsonResponse
from orders.forms import OrderCancellationForm,ReturnreasonForm
from django.contrib import messages

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from Product.models import ProductOffer,Category_offer

from Product.models import Product



# Create your views here.

def Order_success(request):
    if 'user' not in request.session:
        return redirect(user_login)
    
    if request.method == "POST":
        username = request.session['user']
        select_address_id = request.POST.get('address')
        payment = request.POST.get('pay-method')
        coupon = request.POST.get('coupon')
        remove_coupon = request.POST.get('remove_coupon',None)
        print(payment)

        user = get_object_or_404(User, username=username)

        try:
            address = User_address.objects.get(pk=select_address_id)
        except User_address.DoesNotExist:
            return HttpResponse("Error: Address doesn't exist")
        
        try:
            cart = Cart.objects.get(customer_id=user.id)
            cart_items = Cart_items.objects.filter(cart=cart,product__soft_delete=False,product__category__soft_delete=False)
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
            order_items.append({
                'product_id': product.id,
                'quantity': item.quantity,
                'price': float(product_price) 
                })
            print(total_price)

        # total_price=sum( total_price for item in cart_items)
        print(total_price)

        print(order_items)
    
       
        if isinstance(total_price, float):
            print('Total price is of type:', type(total_price))
            total_price = Decimal(total_price)

        coupon_discount = Decimal('0.00')
        if coupon and not remove_coupon:
            print(coupon)
            
            try:
                coupon = Coupon.objects.get(coupon_code=coupon, is_active=True)
                
                if total_price >= coupon.min_purchase_amount:
                    coupon_discount = float(coupon.discount)
                    
                    total_price -= Decimal(coupon_discount)

                    request.session['coupon'] = coupon.coupon_code
                    
                   
                    
                    
                else:
                    return HttpResponse("Error: Minimum purchase amount for the coupon is not met")
            except Coupon.DoesNotExist:
                return HttpResponse("Error: Invalid coupon code")
            # print('after coupon applied total_price',total_price )
            #return JsonResponse({'status':'success'})
        if remove_coupon:
            coupon = None
            messages.success(request,"coupon removed successfully")
            return redirect(Checkout)
        
        
        # if payment == 'cod':
        #     if total_price < 1000:
        #         print('cod above 1000')
        #         messages.error(request,"cash on delivery is not applicable for above 1000 ")
        #         # return  redirect(Checkout)
        
        if payment =='wallet':
            
            wallet = get_object_or_404(Wallet,user=user)
            print(wallet)
            transaction = Transaction.objects.filter(wallet=wallet)
            if wallet.amount>total_price:
                wallet.amount -=Decimal(total_price)
                wallet.save()
                order = Order.objects.create(
                    user =user,
                    created_at =timezone.now(),
                    total_price = total_price,
                    status ='pending',
                    street_address = address.street,
                    city  = address.city,
                    district = address.district,
                    state = address.state,
                    pincode=address.pincode,
                    payment=payment,
                    payment_status='Paid',
                    coupon=coupon if coupon else None 


                )
                for item in order_items:
                    product = get_object_or_404(Product,id = item['product_id'])
                    Order_item.objects.create(
                        order=order,
                        Product=product,
                        quantity=item['quantity'],
                        price=item['price']
                    )

                    product.stock -= item['quantity']
                    product.save()
                cart_items.delete()
                Transaction.objects.create(wallet = wallet,amount = order.total_price,transaction_type = 'debit')

                return render(request, 'order-success.html')
            else:
                return redirect(Checkout)
            

        if payment == 'razorpay':
            print("haii")
            request.session['total_price'] = str(total_price)
            request.session['order_items'] = order_items 
            request.session['address_id'] = select_address_id  
            # request.session['coupon'] = coupon if coupon else None 
            return redirect(paymenthomepage)
        
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
       
    
    
        for item in order_items:
            product = get_object_or_404(Product,id = item['product_id'])
            Order_item.objects.create(
                order=order,
                Product=product,
                quantity=item['quantity'],
                price=item['price']
            )

            product.stock -= item['quantity']
            product.save()
        cart_items.delete()
        
        
        # if payment == 'wallet':
        #     wallet = get_object_or_404(Wallet,user = user)
        #     transaction = Transaction.objects.filter(wallet = wallet)
        #     if wallet.amount > total_price:
        #         wallet.amount -= Decimal(total_price)
        #         wallet.save()
        #         order.payment_status = 'Paid'
        #         order.save()
            
                
        #         Transaction.objects.create(wallet=wallet, amount=total_price, transaction_type='debit')
        #     else:
                
        #         order.delete()
        #         messages.error(request, "insufficient balance in wallet")
            
                
               
        
       
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
                print(' inside reason form ')

                order.status = 'cancel requested'
                order.save()
                Order_cancellation.objects.create(
                    order=order,
                    reason=form.cleaned_data['reason'],
                    cancel_status ='pending'
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
        
        
        print('return')
        if request.method == 'POST':
            print('reason post')
            form = ReturnreasonForm(request.POST)

            if form.is_valid():
                print(' inside reason form ')

                order.is_return=True
                order.return_status = 'Return requested'
                order.save()
                return_reason.objects.create(
                    order=order,
                    return_reason=form.cleaned_data['reason'],
                   
                )

                return redirect(user_profile,pk = user.id)
        else:
            form = ReturnreasonForm()
            return render(request, 'return_reason.html', {'order': order,'form': form})
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
    if 'user' in request.session:
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
                        
                        user = get_object_or_404(User, username=request.session['user'])
                        cart = Cart.objects.get(customer_id=user.id)
                        cart_items = Cart_items.objects.filter(cart=cart)
                        address = User_address.objects.get(id=request.session['address_id'])
                        order_items = request.session.get('order_items',[])
                        coupon_code = request.session.get('coupon', None)
                        coupon = None
                        if coupon_code:
                            try:
                                coupon = Coupon.objects.get(coupon_code=coupon_code, is_active=True)
                            except Coupon.DoesNotExist:
                                coupon = None
                        print('order not created')

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
                            payment='razorpay',
                            payment_status='Paid',
                            coupon=coupon
                        )
                        print('order created order items not')
                        for item in order_items:
                            product = get_object_or_404(Product,id = item['product_id'])
                            Order_item.objects.create(
                                order=order,
                                Product=product,
                                quantity=item['quantity'],
                                price=item['price']
                            )

                            product.stock -= item['quantity']
                            product.save()
                        cart_items.delete()
                        
                        print('order and order items created')
                            
                        del request.session['total_price']
                        del request.session['order_items']
                        del request.session['address_id']
                        # del request.session['coupon']


                        
                        
                        session_data = []
                        for key, value in request.session.items():
                            session_data.append(f'{key}: {value}')
                        
                        session_details = '<br>'.join(session_data)
                        
                        print(session_details)
                        
                        

                        return render(request, 'order-success.html')
                    except Exception as e:
                        print(e)
                        print("payment failed")
                        # if there is an error while capturing payment.
                        return render(request, 'paymentfail.html')
                else:
                    print("failed")
                    messages.error(request,"Payment vaerification failed.please try again")
                    return redirect(Checkout)
            except:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()
    return redirect(user_login)



def order_pdf_view(request,pk):

    # print('pdf')

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

