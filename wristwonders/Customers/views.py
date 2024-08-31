from django.shortcuts import render,redirect,get_object_or_404
from authentication.views import user_login
from Product.models import Category,Product,Category_offer,ProductOffer,Brand
from .models import User,Cart,Cart_items,User_address,Wishlist,Wishlist_items,Wallet,Transaction
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .forms import addaddressform,editaddressform,edituserform
from django.contrib import messages
from orders.models import Order,Order_item
from django.utils import timezone
from decimal import Decimal
from django.db.models import Q

from django.core.paginator import Paginator

# Create your views here.


# home before login

def index_page(request):
    category = Category.objects.all().exclude(soft_delete = True),
    products = Product.objects.all().exclude(soft_delete = True)

    return render(request,'index.html',{'products':products,'category':category})



# home after login

def Home_page(request):
    if request.user.is_authenticated:
        request.session['user'] = request.user.username
        try:
            wallet , created= Wallet.objects.get_or_create(user= request.user)
            wishlist ,created= Wishlist.objects.get_or_create(user=request.user)
        except:
            pass
        category = Category.objects.all().exclude(soft_delete = True),
        products = Product.objects.all().exclude(soft_delete = True)

        return render(request,'home.html',{'products':products,'category':category})
    return redirect(user_login)


def product_detail(request,pk):

    if 'user' in request.session:
        print(request.session['user'])
        username = request.session['user']
        user = get_object_or_404(User, username=username)
        product =get_object_or_404(Product,pk=pk)
        all_products = []
        product_variants = product.variants.all()
        if product_variants:
            all_products =  [product] + list(product_variants)
        print(product_variants,'varient')
        related_products = Product.objects.filter(category=product.category).exclude(pk=pk)
        category_offer = Category_offer.objects.filter(category=product.category,
                                                   start_date__lte=timezone.now(),
                                                   end_date__gte=timezone.now()).first()
    
    
        product_offer = ProductOffer.objects.filter(product=product,
                                                 start_date__lte=timezone.now(),
                                                 end_date__gte=timezone.now()).first()
        try:
            wishlist = Wishlist.objects.get(user= user)
            product_in_wishlist = Wishlist_items.objects.filter(product=product, wishlist=wishlist).exists()
        except Wishlist.DoesNotExist:
            pass

        if category_offer:
        
            category_discounted_price = Decimal(product.price) - (Decimal(product.price) * category_offer.discount_percentage / Decimal(100))

        
    
        if product_offer:
            
            product_discounted_price = Decimal(product.price) - Decimal(product_offer.discount_price)
            
        discounted_price = product.price
        if category_offer and product_offer:
            if category_discounted_price < product_discounted_price:
                discounted_price = category_discounted_price
            else:
                discounted_price = product_discounted_price
        elif category_offer:
            discounted_price = category_discounted_price
        elif product_offer:
            discounted_price = product_discounted_price
        print("dicsount price",discounted_price)
       
        return render(request,'product-page.html',{'product':product,'related_products':related_products,'discounted_price': discounted_price,'product_in_wishlist': product_in_wishlist,'varients':all_products})
    return redirect(user_login)







def view_cart(request):
    if 'user' in request.session:
        try:
            cart = Cart.objects.get(customer=request.user)
            print(cart.id)
            cart_items = Cart_items.objects.filter(cart=cart)
            for item in cart_items:
                
                category_offer = Category_offer.objects.filter(category=item.product.category,
                                                               start_date__lte=timezone.now(),
                                                               end_date__gte=timezone.now()).first()
                
                product_offer=ProductOffer.objects.filter(product=item.product,start_date__lte=timezone.now(),end_date__gte=timezone.now()).first()
                
                
                
                
                if category_offer:
                    category_product_price = Decimal(item.product.price) - (Decimal(item.product.price) * category_offer.discount_percentage / Decimal('100'))
                
                if product_offer:
                    product_product_price=Decimal(item.product.price)-Decimal(product_offer.discount_price)
                    
                if category_offer and product_offer:
                    if category_product_price < product_product_price:
                        item.product.price = category_product_price
                    else:
                        item.product.price = product_product_price
                elif category_offer:
                    item.product.price=category_product_price
                elif product_offer:
                    item.product.price = product_product_price
                    
                else:
                    item.product.price = item.product.price
                
                item.total_price = item.product.price * item.quantity
                print(type(item.total_price))
                for i in cart_items:
                    print(type(i),i)
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
        product = get_object_or_404(Product, pk=pk)
        category_offer = Category_offer.objects.filter(category=product.category,
                                                           start_date__lte=timezone.now(),
                                                           end_date__gte=timezone.now()).first()
        
        product_price = Decimal(product.price)
        if category_offer:
            print("yes inside this")
            category_discounted_price = product_price - (product_price * category_offer.discount_percentage / Decimal(100))
        else:
            product_price = product.price

        cart, created = Cart.objects.get_or_create(customer=user)

        
        cart_item, created = Cart_items.objects.get_or_create(cart=cart, product=product)
        if created:
            cart_item.quantity = 1
        else:
            cart_item.quantity += 1
        cart_item.save()
        return redirect(view_cart)

    return redirect(user_login)

def remove_cart(request, pk):
   
    # print('remove cart')
    if request.method == 'POST' and 'user' in request.session:
        # print('in the remove cart')
        try:
            # print('try')
            username = request.session['user']
            # print(username)
            user = get_object_or_404(User, username=username)
            # print(user)
            # product = get_object_or_404(Product, pk=pk)
            # print(product)
            cart = Cart.objects.get(customer=user)
            cart_item = Cart_items.objects.get(cart=cart, pk = pk)
            
            
            
            # print(cart)
            # print(cart_item)
            

            cart_item.delete()
            return JsonResponse({'success': True})
        except (Cart.DoesNotExist, Cart_items.DoesNotExist, Product.DoesNotExist):
            print('e')
            return JsonResponse({'success': False, 'error': 'Item or cart does not exist'})
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

        cart_items = Cart_items.objects.filter(cart=cart_item.cart)
        
        for item in cart_items:

            category_offer = Category_offer.objects.filter(category=item.product.Category,
                                                           start_date__lte=timezone.now(),
                                                           end_date__gte=timezone.now()).first()
            
            product_offer=ProductOffer.objects.filter(product=item.product,start_date__lte=timezone.now(),end_date__gte=timezone.now()).first()
            
            product_price=None
            
            if category_offer:
                category_product_price = Decimal(item.product.price) - (Decimal(item.product.price) * category_offer.discount_percentage / Decimal('100'))
                
            if product_offer:
                    product_product_price=Decimal(item.product.price)-Decimal(product_offer.discount_price)
                    
            if category_offer and product_offer:
                if category_product_price < product_product_price:
                    product_price = category_product_price
                else:
                    product_price = product_product_price
            elif category_offer:
                    product_price=category_product_price
            elif product_offer:
                    product_price = product_product_price
            else:
                product_price = item.product.price
            
            
            item.total_price = product_price * item.quantity
            item.save()  # Save each item after updating total_price
        
        total_price = sum(item.total_price for item in cart_items)
        

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            total_price = sum(item.get_total() for item in Cart_items.objects.filter(cart=cart_item.cart))
            
            return JsonResponse({'message': 'Item updated', 'cart_total': total_price, 'item_quantity': quantity})
    return JsonResponse({'message': 'Invalid request'})

    



def user_profile(request,pk):
    if 'user' in request.session:
        try:

            user = get_object_or_404(User,id = pk)
            address = User_address.objects.filter(customers_id=user.id)
            orders =  Order.objects.filter(user_id = pk).order_by('-created_at')
            wallet = get_object_or_404(Wallet, user=user)
            transactions = Transaction.objects.filter(wallet=wallet).order_by('-Transaction_date')
            print(wallet)
            # print(orders)

            paginator = Paginator(orders,10)
            page_number  = request.GET.get('page',1)
            orders = paginator.get_page(page_number)

            paginator1 = Paginator(transactions,5)
            page = request.GET.get('page',1)
            transactions = paginator1.get_page(page)
            
            return render(request,'user_profile.html',{'user':user,'address':address,'orders': orders,'wallet':wallet,'transactions':transactions })
        except User.DoesNotExist:
            return redirect(user_login)
    return redirect(user_login)


def edit_user(request,pk):
    if 'user' in request.session:
        username = request.session['user']

        user = get_object_or_404(User,username=username)

        if request.method == 'POST':
            edituser = edituserform(request.POST,instance=user)

            if edituser.is_valid():
                
                edituser.save()

                return redirect(user_profile,pk=user.id)
            else:
                print('user edit form not valid ')
                return render(request,'edituser.html',{'form' : edituser})
        edituser = edituserform(instance = user)    
        return render(request, 'edituser.html',{'form': edituser})
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
                    category_offer = Category_offer.objects.filter(category=item.product.category,
                                                               start_date__lte=timezone.now(),
                                                               end_date__gte=timezone.now()).first()
            
                    product_offer=ProductOffer.objects.filter(product=item.product,start_date__lte=timezone.now(),end_date__gte=timezone.now()).first()
                    
                    if category_offer:
                        category_product_price = Decimal(item.product.price) - (Decimal(item.product.price) * category_offer.discount_percentage / Decimal('100'))
                    if product_offer:
                        product_product_price=Decimal(item.product.price)-Decimal(product_offer.discount_price)
                    
                    if category_offer and product_offer:
                        if category_product_price < product_product_price:
                            product_price = category_product_price
                        else:
                            product_price = product_product_price
                    elif category_offer:
                        product_price=category_product_price
                    elif product_offer:
                        product_price = product_product_price
                    else:
                        product_price = item.product.price
                    
                    item.total_price = product_price * item.quantity
                    
                    # item.total_price = item.product.price * item.quantity


                total_price = sum(item.total_price for item in cart_items)
            return render(request,'check-out.html',{'alladdress':all_address,'products':cart_items,'totalprice':total_price,'cart':cart,'user':user})
        except Cart_items.DoesNotExist:
            return redirect(view_cart)
        except User.DoesNotExist:
            return redirect(user_login)
        
    return redirect(user_login)
        


def all_products(request):

    active_category = Category.objects.filter(soft_delete = False)
    products = Product.objects.filter(category__in = active_category,soft_delete = False)
    brand = Brand.objects.all()
    search = request.GET.get('search','')
    sort_by = request.GET.get('sort','name')
    filter_by_category = request.GET.get('filter_by_category')
    filter_by_brand =request.GET.get('filter_by_brand')
    # print(products)
    
    print('sort')
    print(search, 'search')
    if search:
        products = Product.objects.filter(Product_name__icontains = search )
        # print(products)



#  filter 
    
        
    if filter_by_category:

        products = products.filter(category__category_name = filter_by_category)

    if filter_by_brand:
        products = products.filter(brand__name=filter_by_brand) 
    
    #  sorting
    if sort_by== 'aA-zZ':
        print('n')
        products = products.order_by('Product_name')
    elif sort_by == 'zZ-aA':
        print('-n')
        products =products.order_by('-Product_name')

    elif sort_by == 'high-low':
        products = products.order_by('-price')
    elif sort_by == 'low-high':
        products=products.order_by('price')
    
    else:
       products = products
    
    paginator =  Paginator(products,8)
    page_number = request.GET.get('page',1)
    products = paginator.get_page(page_number)
    return render(request,'allproducts.html',{'products':products,'category':active_category,'brand':brand})



def user_order_details(request,pk):
    if 'user' in request.session:
        username = request.session['user']
        user = get_object_or_404(User,username=username)
        user_id = user.id
        order = get_object_or_404(Order,id=pk)
        order_items = Order_item.objects.filter(order_id = order.id)
        total_order_price = sum(item.price for item in order_items)
        return render(request,'userorderdetails.html',{'order':order,'order_items':order_items,'total_order_price':total_order_price,'user':user})
    return redirect(user_login)


def wish_list(request):
    if 'user' in request.session:
        username = request.session['user']
        user = get_object_or_404(User,username=username)
        wishlist = get_object_or_404(Wishlist,user = user)
        wishlist_items = Wishlist_items.objects.filter(wishlist=wishlist)

        return render(request,'wishlist.html',{'wishlist':wishlist,'wishlistitems':wishlist_items})
    return redirect(user_login)


def add_wishlist(request,pk):
    print('add to wishlist')
    if 'user' in request.session:
        username = request.session['user']
        user = get_object_or_404(User,username=username)
        product = get_object_or_404(Product,pk=pk)

        wishlist,created = Wishlist.objects.get_or_create(user = user)
        wishlist_item,created = Wishlist_items.objects.get_or_create(product=product, wishlist=wishlist)
        return JsonResponse({'status': 'success', 'message': 'Added to wishlist'})
    return JsonResponse({'status': 'error', 'message': 'User not logged in'})

    #     return redirect(wish_list)
    # return redirect(user_login)

def remove_wishlist(request,pk):
    if 'user' in request.session:
        username = request.session['user']
        user = get_object_or_404(User, username=username)
        product = get_object_or_404(Product, pk=pk)

        try:
            wishlist = Wishlist.objects.get(user=user)
            wishlistitem = Wishlist_items.objects.get(product=product, wishlist=wishlist)
            wishlistitem.delete()
        except Wishlist_items.DoesNotExist:
            # If the item does not exist, handle it gracefully
            return redirect('wishlist')  # Redirect to the wishlist page

        return redirect('wishlist')  # Redirect to the wishlist page
    else:
        return redirect('user_login')




def add_funds(request):
    user = request.user
    wallet = get_object_or_404(Wallet, user=user)
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount:
            amount = Decimal(amount)

            wallet.amount += amount
            wallet.save()
            Transaction.objects.create(wallet=wallet, amount=amount, transaction_type='credit')
            messages.success(request, f'Successfully added ${amount} to your wallet.')
            return redirect(user_profile,pk = user.id)
    
    return render(request, 'add_funds.html', {'wallet': wallet})



def change_password(request):
    if 'user' in request.session:
        pass

        
