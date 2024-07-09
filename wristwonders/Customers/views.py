from django.shortcuts import render,redirect,get_object_or_404
from authentication.views import user_login
from Product.models import Category,Product
from .models import User,Cart,Cart_items,User_address
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .forms import addaddressform,editaddressform
from django.contrib import messages
from orders.models import Order,Order_item

# Create your views here.


# home before login

def index_page(request):
    category = Category.objects.all().exclude(soft_delete = True),
    products = Product.objects.all().exclude(soft_delete = True)

    return render(request,'index.html',{'products':products,'category':category})



# home after login

def Home_page(request):
    if request.user.is_authenticated:
        category = Category.objects.all().exclude(soft_delete = True),
        products = Product.objects.all().exclude(soft_delete = True)

        return render(request,'home.html',{'products':products,'category':category})
    return redirect(user_login)


def product_detail(request,pk):

    if 'user' in request.session:
        print(request.session['user'])
        product =get_object_or_404(Product,pk=pk)
        related_products = Product.objects.filter(category=product.category).exclude(pk=pk)
        return render(request,'product-page.html',{'product':product,'related_products':related_products})
    return redirect(user_login)






def view_cart(request):
    if 'user' in request.session:
        try:
            cart = Cart.objects.get(customer=request.user)
            cart_items = Cart_items.objects.filter(cart=cart)
            total_price = sum(item.get_total() for item in cart_items)
        except Cart.DoesNotExist:
            cart_items = []
            total_price = 0
        return render(request, 'shopping-cart.html', {'cart_items': cart_items, 'total_price': total_price})
    return redirect(user_login)

def add_to_cart(request, pk):
    if 'user' in request.session:
        username = request.session['user']
        user = get_object_or_404(User, username=username)

        cart, created = Cart.objects.get_or_create(customer=user)

        product = get_object_or_404(Product, pk=pk)
        cart_item, created = Cart_items.objects.get_or_create(cart=cart, product=product)
        if created:
            cart_item.quantity = 1
        else:
            cart_item.quantity += 1
        cart_item.save()
        return redirect(view_cart)

    return redirect(user_login)

def remove_cart(request, pk):
    if 'user' in request.session:
        try:
            username = request.session['user']
            user = get_object_or_404(User, username=username)
            product = get_object_or_404(Product, pk=pk)
            cart = Cart.objects.get(customer=user)
            cart_item = Cart_items.objects.get(cart=cart, product=product)

            cart_item.delete()
            return JsonResponse({'success': True})
        except Cart.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cart does not exist'})
    return JsonResponse({'success': False, 'error': 'User not logged in'})

def update_cart(request, pk):
    if request.method == "POST":
        cart_item = get_object_or_404(Cart_items, pk=pk)
        quantity = int(request.POST.get('quantity', 1))

        if quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()

        if request.is_ajax():
            total_price = sum(item.get_total() for item in Cart_items.objects.filter(cart=cart_item.cart))
            return JsonResponse({'message': 'Item updated', 'cart_total': total_price, 'item_quantity': quantity})
    return JsonResponse({'message': 'Invalid request'})

    

def user_profile(request,pk):
    if 'user' in request.session:
        try:

            user = get_object_or_404(User,id = pk)
            address = User_address.objects.filter(customers_id=user.id)
            orders =  Order.objects.filter(user_id = pk).order_by('-created_at')
            # print(orders)
            
            return render(request,'user_profile.html',{'user':user,'address':address,'orders': orders })
        except User.DoesNotExist:
            return redirect(user_login)
    return redirect(user_login)


def add_address(request):
    if 'user' in request.session:
        username = request.session['user']

        user = get_object_or_404(User,username=username)

        if request.method == 'POST':
            addressform = addaddressform(request.POST,request.FILES)
            if addressform.is_valid():
                phone = addressform.cleaned_data['phone_no']
                print(phone)
                try:
                    form = addressform.save(commit=False)
                    form.customers_id=user.id
                    form.save()
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)

                    return redirect(user_profile,pk=user.id)
                except Exception as e:
                    print('error in saving :',e)
            else:
                print('form is not valid')
                return render(request,'add-address.html',{'f':addressform})
            
        addaddress=addaddressform()
        return render(request,'add-address.html',{'f':addaddress})
    return redirect(user_login)

                

        

def editaddress(request,pk):
    if 'user' in request.session:
        username = request.session['user']
        user = get_object_or_404(User,username=username)
        try:
            address = get_object_or_404(User_address,id = pk)
        except User_address.DoesNotExist:
            return redirect(user_profile)
        if request.method == 'POST':
            form = editaddressform(request.POST,instance=address)
            if form.is_valid():
                try:
                   
                    
                    form.save()
                    return redirect(user_profile,pk=user.id)
                except Exception as e:
                    print('error in saving :',e)
            else:
                print('form is not valid')
                return render(request,'add-address.html',{'f':form})
                
        editaddress =editaddressform(instance=address)
        return render(request,'edit-address.html',{'f':editaddress})
    
    return redirect(user_login)

def delete_address(request,pk):
    if 'user' in request.session:
        username = request.session['user']
        user = get_object_or_404(User,username=username)
        address = get_object_or_404(User_address,id=pk)

        address.delete()
        return redirect(user_profile,pk=user.id)
    return redirect(user_login)





def Checkout(request):
    if 'user' in request.session:
        try:
            username = request.session['user']
            user = get_object_or_404(User,username=username)
            user_id = user.id
            # getting all the address of user
            all_address = User_address.objects.filter(customers_id=user_id)

            # getting the cart

            cart = Cart.objects.get(customer_id = user.id)
            cart_items = Cart_items.objects.filter(cart = cart)

            if cart_items.exists():
                for item in cart_items:

                    if item.quantity > item.product.stock:
                        messages.error(request,f"Quantity for {item.product.Product_name}.exceeds available stock")
                        return redirect(view_cart)
                    
                    item.total_price = item.product.price * item.quantity


                total_price = sum(item.total_price for item in cart_items)
            return render(request,'check-out.html',{'alladdress':all_address,'products':cart_items,'totalprice':total_price,'cart':cart,'user':user})
        except Cart_items.DoesNotExist:
            return redirect(view_cart)
        except User.DoesNotExist:
            return redirect(user_login)
        
    return redirect(user_login)
        


def all_products(request):
    products = Product.objects.all()

    return render(request,'allproducts.html',{'products':products})

# def allcategories(request):
#     categories = Category.objects.all()
#     return render(request,'nav.html',{'categories':categories})
# 