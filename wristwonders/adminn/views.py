from django.shortcuts import render,redirect,get_object_or_404
from authentication.views import admin_login
from Customers.models import User
from authentication.forms import RegisterForm
from .forms import UpdateForm,AddCouponForm,EditCouponForm
from orders.models import Order,Order_item
from django.http import JsonResponse
from .models import Coupon
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.http import require_POST
from decimal import Decimal

# Create your views here.


def admin_home(request):
    if request.user.is_authenticated:
        return render(request,'admin_home.html')
    return redirect(admin_login)


def User_list(request):
   if 'adminn' in request.session:
       user = User.objects.all()
       return render(request,'users.html',{'user':user})
   return redirect(admin_login)


def add_user(request):
    if 'adminn' in request.session:
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                print(user)
                return redirect('adminn-user-list')
        else:
            form = RegisterForm()
        return render(request,'add-user.html',{'form':form})
    return redirect(admin_login)

def Update_user(request,pk):
    if 'adminn' in request.session:
        instance = User.objects.get(id=pk)
        form = UpdateForm(instance=instance)
        if request.POST:
            fm = UpdateForm(request.POST,instance=instance)
            if fm.is_valid:
                fm.save()
                return redirect('adminn-user-list')
            else:
                form=UpdateForm(instance=instance)
        return render(request,'update-user.html',{'form':form})
    return redirect(admin_login)

# block user
def block_user(request,pk):
    if 'adminn' in request.session:
        instance = User.objects.get(id =pk)
        instance.is_active = False
        instance.save()
        return redirect('adminn-user-list')
    return redirect(admin_login)


# unblock user
def Un_block_user(request,pk):
    if 'adminn' in request.session:
        instance = User.objects.get(id =pk)
        instance.is_active = True
        instance.save()
        return redirect('adminn-user-list')
    return redirect(admin_login)



def orders_list(request):
    if 'adminn' in request.session:
        if request.method == "POST":
            order_id = request.POST.get('order_id')
            new_status = request.POST.get('new_status')
            print(order_id)
            print(new_status)
            try:
                order = Order.objects.get(pk=order_id)
                print(order.user)
                if order.is_return:
                    order.return_status=new_status
                    if new_status == 'Returned':
                        order.payment_status = 'cash refunded'
                        order.save()
                    order.save()
                
                if new_status == 'Delivered':
                    order.payment_status='Paid'
                    order.save()

                if new_status =="Cancelled":
                    print("order cancelled")
                    order_items=Order_item.objects.filter(order=order)
                    for item in order_items: 
                        item.product.quantity += item.quantity
                        item.product.save()
                if not order.is_return:
                    
                    order.status = new_status
                    order.save()
                return JsonResponse({'success': True})
            except Order.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Order does not exist'})
        orders = Order.objects.all().order_by('-created_at')
        return render(request,'adminnorders.html',{'orders':orders})
    return redirect(admin_login)


def order_detail(request,pk):
    if 'adminn' in request.session:
        order = get_object_or_404(Order,id=pk)
        order_items = Order_item.objects.filter(order_id = order.id)
        total_order_price = sum(item.price for item in order_items)
        return render(request,'adminnorderdetail.html',{'order':order,'order_items':order_items,'total_order_price':total_order_price})
    return redirect(admin_login)



# @csrf_exempt
# @require_POST
# def admin_order_status_update(request):
#     try:
#         order_id = request.POST.get('order_id')
#         new_status = request.POST.get('new_status')
#         update_type = request.POST.get('update_type')

#         order = get_object_or_404(Order, id=order_id)

#         if update_type == 'order_status':
#             order.status = new_status
#         elif update_type == 'return_status':
#             order.return_status = new_status

#         order.save()
#         return JsonResponse({'success': True})

#     except Exception as e:
#         return JsonResponse({'success': False, 'error': str(e)})



def coupon_list(request):
    if 'adminn' in request.session:
        coupons = Coupon.objects.all()
        return render(request,'coupon.html',{'coupons':coupons})
    return redirect(admin_login)


def addcoupon(request):
    if 'adminn' in request.session:
        if request.method == "POST":
            addcoupon_form = AddCouponForm(request.POST)
            if addcoupon_form.is_valid():
                couponcode=addcoupon_form.cleaned_data['coupon_code']
                discount=addcoupon_form.cleaned_data['discount']
                min_purchase_amount=addcoupon_form.cleaned_data['min_purchase_amount']

                if len(couponcode)<6:               
                    addcoupon_form.add_error('coupon_code','it should be length more than 6')
                
                if discount < 1.00:
                    addcoupon_form.add_error('discount','discount should be greater than 0')
                
                if min_purchase_amount < 10.00:
                    addcoupon_form.add_error('min_purchase_amount','amount should be greater than 10')
                
                if discount >= min_purchase_amount:
                    addcoupon_form.add_error('discount','discount amount should be lesser than min purchase amount')
                    
                if Coupon.objects.filter(coupon_code=couponcode).exists():
                    print("coupon exists")
                    addcoupon_form.add_error('coupon_code','this coupon code already exists')
                    
                if addcoupon_form.errors:
                    return render(request,'addcoupon.html',{'form':addcoupon_form})
                
                else:
                    
                    addcoupon_form.save()
                    return redirect(coupon_list)
            else:
                
                return render(request, 'addcoupon.html', {'form': addcoupon_form})
        form=AddCouponForm()
        return render(request,'addcoupon.html',{'form':form})
    return redirect(admin_login)


def edit_coupon(request,pk):
    if 'adminn' in request.session:
        coupon = get_object_or_404(Coupon, id=pk) 
        if request.method =="POST":
            print('inside coiupon post')
            print('Request POST data:', request.POST)
            editcoupon_form = EditCouponForm(request.POST,instance=coupon)
            
            if editcoupon_form.is_valid():
                print('form valid')
                couponcode=editcoupon_form.cleaned_data['coupon_code']
                discount=editcoupon_form.cleaned_data['discount']
                min_purchase_amount=editcoupon_form.cleaned_data['min_purchase_amount']

                if len(couponcode)<6:               
                    editcoupon_form.add_error('coupon_code','it should be length more than 6')
                
                if discount < 1.00:
                    editcoupon_form.add_error('discount','discount should be greater than 0')
                
                if min_purchase_amount < 10.00:
                    editcoupon_form.add_error('min_purchase_amount','amount should be greater than 10')
                
                if discount >= min_purchase_amount:
                    editcoupon_form.add_error('discount','discount amount should be lesser than min purchase amount')
                    
                
                    
                if editcoupon_form.errors:
                    return render(request,'editcoupon.html',{'form':editcoupon_form})
                
                else:
                    print('coupon save')
                    editcoupon_form.save()
                    return redirect(coupon_list)
            
            else:
                print('Form is invalid')
                print('Form errors:', editcoupon_form.errors)
                return render(request, 'editcoupon.html', {'form': editcoupon_form})
        form = EditCouponForm(instance=coupon)
        return render(request,'editcoupon.html',{'form':form})
    return redirect(admin_login)


def deletecoupon(request,pk):
    if 'adminn' in request.session:
        coupon = get_object_or_404(Coupon,id=pk)
        coupon.delete()
        return redirect(coupon_list)
    return redirect(admin_login)


@csrf_exempt
def apply_coupon(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            coupon_code = request.POST.get('coupon')
            total_price = request.POST.get('totalprice') # Convert to Decimal for precise calculations
            if total_price is None:
                return JsonResponse({
                    'status':'error',
                    'message':'error:total_price is null'

                })

            try:
                total_price = Decimal(total_price)
                coupon = Coupon.objects.get(coupon_code=coupon_code, is_active=True)
                if total_price >= coupon.min_purchase_amount:
                    new_total_price = total_price - coupon.discount
                    return JsonResponse({
                        'status': 'success',
                        
                        'new_total_price': float(new_total_price)  
                    })
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': "Error: Minimum purchase amount for the coupon is not met"
                    })
            except Coupon.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': "Error: Invalid coupon code"
                })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request'
    })