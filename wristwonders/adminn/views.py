from django.shortcuts import render,redirect,get_object_or_404
from authentication.views import admin_login
from Customers.models import User
from authentication.forms import RegisterForm
from .forms import UpdateForm
from orders.models import Order,Order_item
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.http import require_POST

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
        order = Order.objects.get(id = pk)
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
