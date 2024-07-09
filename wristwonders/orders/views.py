from django.shortcuts import render,get_object_or_404,redirect
from Customers.models import User,User_address
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from Customers.models import Cart,Cart_items
from Customers.views import Checkout,user_profile
from authentication.views import user_login
from django.utils import timezone
from .models import Order,Order_item




# Create your views here.

def Order_success(request):
    if 'user' not in request.session:
        return redirect(user_login)
    
    if request.method == "POST":
        username = request.session['user']
        select_address_id = request.POST.get('address')
        payment = request.POST.get('pay-method')

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

            if item.quantity > product.stock:
                print('stock limit exceeds')
                
                return redirect(Checkout)
            
            total_price += item.quantity * product.price
            order_items.append((product, item.quantity, product.price))

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
            payment_status='Pending'
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
        return render(request, 'order-success.html')
    
    return redirect(Checkout)


def ordercancel(request,pk):
    if 'user' in request.session:
        username = request.session['user']
        user = User.objects.get(username  = username)

        order = Order.objects.get(id = pk)
        orderitem = Order_item.objects.filter(order_id = order.id)

        for item in orderitem:
            item.Product.stock +=item.quantity
            item.Product.save()
        
        order.is_cancelled = True
        order.save()

        return redirect(user_profile,pk = user.id)
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
