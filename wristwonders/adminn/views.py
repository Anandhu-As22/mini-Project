from django.shortcuts import render,redirect,get_object_or_404
from authentication.views import admin_login
from Customers.models import User,Wallet,Transaction
from authentication.forms import RegisterForm
from .forms import UpdateForm,AddCouponForm,EditCouponForm,ProductOfferForm,CategoryOfferForm,EditCategoryOfferForm,EditProductOffersForm
from orders.models import Order,Order_item,Order_cancellation
from django.http import JsonResponse
from .models import Coupon,SalesReport

from django.views.decorators.csrf import csrf_exempt
from Product.models import Category_offer,ProductOffer,Product,Category
from django.views.decorators.cache import never_cache

from django.views.decorators.http import require_POST
from decimal import Decimal

from django.core.paginator import Paginator

from django.db.models import Sum,Count
from django.utils import timezone
from datetime import timedelta,datetime
from django.db.models import Q
from  django.db.models.functions import TruncDay,TruncMonth,TruncYear

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.template.loader import render_to_string


import io
import calendar
# Create your views here


def admin_home(request):
    if request.user.is_authenticated:
        user =request.user

        total_sale = Order.objects.filter(status='Delivered',is_cancelled = False).count()

        total_amount = Order.objects.filter(status = 'Delivered',is_cancelled = False).aggregate(total_price=Sum('total_price'))

        total_price = total_amount['total_price']
        orders = Order.objects.order_by('-created_at')[:5]
        customers = User.objects.order_by('-date_joined')[:5]

       


        
       

        users = User.objects.count()
        # print(total_price)
        # print(total_sale)
        # print(user.username)

        top_products = Order_item.objects.values('Product').annotate(order_count = Count('id')).filter(order__status='Delivered',order__is_cancelled=False).order_by('-order_count')[:10]

        top_products_with_details = [{ 'product' : Product.objects.get(id = item['Product']),'order_count':item['order_count']} for item in top_products]

        top_category = Order_item.objects.values('Product__category').annotate(order_count = Count('id')).filter(order__status ='Delivered',order__is_cancelled = False).order_by('-order_count')[:10]

        top_category_with_details = [{'category': Category.objects.get(id=item['Product__category']),'order_count': item['order_count']} for item in top_category]

        # print(top_products,'top')
        # print(top_category,'top category')

        # period = request.GET.get('period')
        # start_date = end_date = timezone.now()

        # if period == 'daily':
        #     start_date = timezone.now().replace(hour=00,minute=00,second=00)
        # elif period == 'weekly':
        #     start_date = timezone.now() - timedelta(days=timezone.now().weekday())
        #     start_date = start_date.replace(hour=00,minute=00,second=00)
        #     end_date = start_date + timedelta(days=6)
        # elif period == 'monthly':
        #     start_date = timezone.now().replace(day=1,hour=00,minute=00,second=00)
        #     last_day_of_month = calendar.monthrange(start_date.year, start_date.month)[1]
        #     end_date = start_date.replace(day=last_day_of_month, hour=23, minute=59, second=59, microsecond=999999)


        # elif period == 'custom':
        #     start_date_date = request.GET.get('start_date')
        #     end_date_date = request.GET.get('end_date')

        #     # Validate that both dates are provided
        #     if not start_date_date or not end_date_date:
        #         # You can handle the missing dates here
        #         return render(request, 'sales.html', {'error': 'Please provide both start and end dates for the custom period.'})

        #     # Parse the custom date inputs
        #     start_date = datetime.strptime(start_date_date, '%Y-%m-%d').replace(hour=0, minute=0, second=0, microsecond=0)
        #     end_date = datetime.strptime(end_date_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59, microsecond=999999)


        # delivered_orders = Order.objects.filter(created_at__range = [start_date,end_date],status ='Delivered' ).filter(Q(is_return = False)|Q(return_status = 'Rejected'))

        # total_sales_delivered = delivered_orders.aggregate(total_sales = Sum('total_price'))['total_sales'] or ()

        # delivery_order_count = delivered_orders.count()

        today = timezone.now()

        start_date = today-timedelta(days=7)

        daily_sales = (Order.objects.filter(status='Delivered', created_at__gte=start_date)
               .annotate(day=TruncDay('created_at'))
               .values('day')
               .annotate(totalSales=Sum('total_price'))
               .order_by('day'))
        # print(daily_sales)

        monthly_sale = (Order.objects.filter(status='Delivered')
                        .annotate(month=TruncMonth('created_at'))
                        .values('month')
                        .annotate(total_sales=Sum('total_price'))
                        .order_by('month'))       
        # print(monthly_sale)
        yearly_sales = (Order.objects
             .annotate(year=TruncYear('created_at'))
             .values('year')
             .annotate(totalSales=Sum('total_price'))
             .order_by('year'))
        print(yearly_sales)


        return render(request,'admin_home.html',{'total_sale' : total_sale,'total_price':total_price,'users' : users,'user':user,'orders':orders,'customers':customers,'top_products':top_products_with_details,'top_category':top_category_with_details,'daily_sales':daily_sales,'monthly_sale':monthly_sale,'yearly_sales':yearly_sales })
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
        search = request.GET.get('q', '')
        print(search)
        if request.method == "POST":
            order_id = request.POST.get('order_id')
            new_status = request.POST.get('new_status')
            print(order_id)
            print(new_status)
            try:
                order = Order.objects.get(pk=order_id)
                wallet = get_object_or_404(Wallet,user = order.user)
                print(order.user)
                if order.is_return:
                    order.return_status=new_status
                    if new_status == 'Returned':
                       

                        wallet.amount += Decimal(order.total_price)
                        wallet.save()
                        Transaction.objects.create(wallet = wallet,amount = order.total_price,transaction_type = 'credit')

                        order.payment_status = 'cash refunded to your wallet'
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
        if search:
            orders = orders.filter(
                Q(id__icontains=search) | 
                Q(user__username__icontains=search) |  
                Q(status__icontains=search)  
            )
        paginator = Paginator(orders,15)
        page_number  = request.GET.get('page',1)
        orders = paginator.get_page(page_number)

        
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

                if Coupon.objects.exclude(id = coupon.pk).filter(coupon_code=couponcode).exists():
                    print("coupon exists")
                    editcoupon_form.add_error('coupon_code','this coupon code already exists')
                
                    
                
                    
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
                    response_data = {
                        'status': 'success',
                        'coupon_code': coupon.coupon_code,
                        'discount': coupon.discount,
                        'new_total_price': new_total_price
                        }
                    return JsonResponse(response_data)
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


def categoryoffers(request):
    if 'adminn' in request.session:
        
        categoryoffers=Category_offer.objects.all()
        return render(request,'admin-categoryoffers.html',{'categoryoffers':categoryoffers})
    return redirect(admin_login)

def add_category_offer(request):
    if 'adminn' in request.session:
        if request.method=='POST':
            form=CategoryOfferForm(request.POST)
            if form.is_valid():
                
                discount_percentage=form.cleaned_data['discount_percentage']
                start_date=form.cleaned_data['start_date']
                end_date=form.cleaned_data['end_date']
                category=form.cleaned_data['category']
                
                
                
                if discount_percentage < 1 :
                    form.add_error('discount_percentage','discount percentage should not less than 0')
                
                if discount_percentage > 90 :
                    form.add_error('discount_percentage','discount percentage should not greater than 90%')
                    
                if start_date > end_date:
                    form.add_error('end_date','end date should be greater than start date')
                
                if Category_offer.objects.filter(category=category).exists():
                    form.add_error('category','offer for this category already exist')
                    
                if form.errors:
                    return render(request,'add_category_offer.html',{'form':form})
                form.save()
                return redirect('category-offers')
        
        else:
                
            form=CategoryOfferForm()
        return render(request,'add_category_offer.html',{'form':form})
    return redirect(admin_login)


def editCategoryOffer(request,pk):
    if 'adminn' in request.session:
        instance_to_be_edited=Category_offer.objects.get(id=pk)
        if request.POST:
            form=EditCategoryOfferForm(request.POST,instance=instance_to_be_edited)
            
            if form.is_valid():
                discount_percentage=form.cleaned_data['discount_percentage']
                start_date=form.cleaned_data['start_date']
                end_date=form.cleaned_data['end_date']
                category=form.cleaned_data['category']
                
                if discount_percentage < 1:
                    form.add_error('discount_percentage','should greater than 0')
                    
                if discount_percentage > 90 :
                    form.add_error('discount_percentage','discount percentage should not greater than 90%')
                    
                if start_date > end_date:
                    form.add_error('end_date','end date should be greater than start date')
                    
                # if Category_offer.objects.filter(category=category).exists():
                #     form.add_error('category','offer for this category already exist')

                if form.errors:
                    return render(request,'admin-edit-Categoryofferform.html',{'form':form})
                
                
                form.save()
                return redirect('category-offers')
        else:
                    
            form=EditCategoryOfferForm(instance=instance_to_be_edited)
        return render(request,'admin-edit-Categoryofferform.html',{'form':form})
    return redirect(admin_login)

@never_cache
def deleteCategoryOffer(request,pk):
    if 'adminn' in request.session:
        category_offer=Category_offer.objects.get(id=pk)
        category_offer.delete()
        return redirect(categoryoffers)
    return redirect(admin_login)


@never_cache
def productoffers(request):
    if 'adminn' in request.session:
        productoffers=ProductOffer.objects.all()
        
        return render(request,'admin-productoffers.html',{'productoffers':productoffers})
    return redirect(admin_login)

@never_cache
def add_product_offer(request):
    if 'adminn' in request.session:
        if request.method=='POST':
            form=ProductOfferForm(request.POST)
            if form.is_valid():
                discount_price=form.cleaned_data['discount_price']
                product=form.cleaned_data['product']
                start_date=form.cleaned_data['start_date']
                end_date=form.cleaned_data['end_date']
                
                
                if discount_price < 0:
                    form.add_error('discount_price','should greater than 0')
                
                if discount_price >= product.price:
                    form.add_error('discount_price','should not be greater than or equal to product price')
                
                if start_date > end_date:
                    form.add_error('end_date','end date should be greater than start date')
                    
                if form.errors:
                    return render(request,'admin-add-product-offer.html',{'form':form})
                form.save()
                return redirect(productoffers)
        form=ProductOfferForm()
        return render(request,'admin-add-product-offer.html',{'form':form})
    return redirect(admin_login)

@never_cache
def editProductOffers(request,pk):
    if 'adminn' in request.session:
        instance_to_be_edited=ProductOffer.objects.get(id=pk)
        if request.POST:
            form=EditProductOffersForm(request.POST,instance=instance_to_be_edited)
            if form.is_valid():
                discount_price=form.cleaned_data['discount_price']
                start_date=form.cleaned_data['start_date']
                end_date=form.cleaned_data['end_date']
                
                print("discount",discount_price)
                if discount_price < 1:
                    form.add_error('discount_price','price should be greater than 0')
                    
                if start_date > end_date:
                    form.add_error('end_date','end date should be greater than start date')
                
                if form.errors:
                    return render(request,'admin-EditProductOffers.html',{'form':form})
                form.save()
                return redirect(productoffers)

        form=EditProductOffersForm(instance=instance_to_be_edited)
        return render(request,'admin-EditProductOffers.html',{'form':form})
    return redirect(admin_login)

@never_cache
def deleteProductOffer(request,pk):
    if 'adminn' in request.session:
        product_offer=ProductOffer.objects.get(id=pk)
        product_offer.delete()
        return redirect(productoffers)
    return redirect(admin_login)






def manage_cancellations(request):
    if 'adminn' in request.session:
        pending_cancellations = Order_cancellation.objects.filter(cancel_status = 'pending')

        return render(request,'manage_cancellations.html',{'pending_cancellations':pending_cancellations})
    return redirect(admin_login)


def approve_cancellations(request,pk):
    if 'adminn' in request.session:
        cancellation = get_object_or_404(Order_cancellation,id = pk)
        order = cancellation.order

        order_items = Order_item.objects.filter(order=order)

        for item in order_items:
            item.Product.stock += item.quantity
            item.Product.save()

        order.is_cancelled = True
        order.save()

        if order.payment_status == 'Paid':
            print('inside paid')
            wallet = get_object_or_404(Wallet,user = order.user)
            print(wallet)
        
            wallet.amount += Decimal(order.total_price)
            wallet.save()

            order.payment_status = 'refunded to wallet'
            order.save()
            

            Transaction.objects.create(wallet = wallet,amount = order.total_price,transaction_type = 'credit')

        cancellation.cancel_status = 'approved'
        cancellation.save()
        return redirect(manage_cancellations)
    return redirect(admin_login)


def reject_cancellation(request,pk):
    if 'adminn' in request.session:
        print('reject')
        cancellation = get_object_or_404(Order_cancellation,id = pk)
        cancellation.cancel_status = 'rejected'
        cancellation.save()
        print(cancellation.cancel_status)
        
        order = cancellation.order
        order.is_cancelled = False
        order.status = 'cancel rejected'
        order.save()
        print(order.is_cancelled)
        return redirect(manage_cancellations)
    return redirect(admin_login)


def sales_report(request):
    if 'adminn' in request.session:
        if request.method == 'POST':
            period = request.POST.get('period')

            start_date = end_date = timezone.now()

            if period == 'daily':
                start_date = timezone.now().replace(hour=00,minute=00,second=00)
            elif period == 'weekly':
                start_date = timezone.now() - timedelta(days=timezone.now().weekday())
                start_date = start_date.replace(hour=00,minute=00,second=00)
                end_date = start_date + timedelta(days=6)
            elif period == 'monthly':
                start_date = timezone.now().replace(day=1,hour=00,minute=00,second=00)
                last_day_of_month = calendar.monthrange(start_date.year, start_date.month)[1]
                end_date = start_date.replace(day=last_day_of_month, hour=23, minute=59, second=59, microsecond=999999)


            elif period == 'custom':
                start_date_date = request.POST.get('start_date')
                end_date_date = request.POST.get('end_date')

                # Validate that both dates are provided
                if not start_date_date or not end_date_date:
                    # You can handle the missing dates here
                    return render(request, 'sales.html', {'error': 'Please provide both start and end dates for the custom period.'})

                # Parse the custom date inputs
                start_date = datetime.strptime(start_date_date, '%Y-%m-%d').replace(hour=0, minute=0, second=0, microsecond=0)
                end_date = datetime.strptime(end_date_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59, microsecond=999999)


            delivered_orders = Order.objects.filter(created_at__range = [start_date,end_date],status ='Delivered' ).filter(Q(is_return = False)|Q(return_status = 'Rejected'))

            total_sales_delivered = delivered_orders.aggregate(total_sales = Sum('total_price'))['total_sales'] or ()

            delivery_order_count = delivered_orders.count()

            coupon_discount = delivered_orders.filter(coupon__isnull=False).aggregate(total_discount = Sum('coupon__discount'))['total_discount'] or ()

            total_actual_price = 0
            product_details = []

            for order in delivered_orders:
                order_items = order.order_item_set.all()

                for item in order_items:
                    actual_price = item.Product.price
                    item_total_price = actual_price * item.quantity
                    total_actual_price += item_total_price


                    product_details.append({
                        'order_id': order.id,
                        'product_name': item.Product.Product_name,
                        'quantity': item.quantity,
                        'actual_price': float(actual_price),
                        'total_price': float(item_total_price)
                    })

            total_discount = total_actual_price - float(total_sales_delivered)

            total_offer_discount = total_discount - float(coupon_discount) 
            # print(total_offer_discount)
            report = SalesReport.objects.create(
                admin_user=request.user,
                start_date=start_date,
                end_date=end_date,
                total_sales_delivered=total_sales_delivered,
                delivery_order_count=delivery_order_count,
                coupon_discount=coupon_discount,
                total_actual_price=total_actual_price,
                total_offer_discount=total_offer_discount
            )
            

            context = { 
                'delivered_orders':delivered_orders,
                'total_sales_delivered': total_sales_delivered,
                'delivery_order_count': delivery_order_count,
                'coupon_discount': coupon_discount,
                'start_date': start_date,
                'end_date': end_date,
                'total_actual_price_of_product': total_actual_price,
                'total_offer_discount': total_offer_discount,
                'report': report
            }
            print(report.id)

            
            return render(request,'sales_report.html',context)      
        return render(request,'sales.html')
    return redirect(admin_login)



def render_to_pdf(template_src, context_dict):
    
    template = render_to_string(template_src, context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(template.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def download_sales_report_pdf(request,pk):
    print('haii')
    if 'adminn' in request.session:
        
        
        try:
            print('try')
            print(pk)
            report = SalesReport.objects.get(pk=pk, admin_user=request.user)
            print(report)
        except SalesReport.DoesNotExist:
            return HttpResponse("Error: Sales report not found", status=400)

       

        # Parse the stored data
        start_date = report.start_date
        end_date = report.end_date

        delivered_orders = Order.objects.filter(created_at__range = [start_date,end_date],status ='Delivered' ).filter(Q(is_return = False)|Q(return_status = 'Rejected'))
        context = {
            'delivered_orders': delivered_orders,  # Fetch or leave empty if not needed
            'total_sales_delivered': report.total_sales_delivered,
            'delivery_order_count': report.delivery_order_count,
            'coupon_discount': report.coupon_discount,
            'start_date': report.start_date,
            'end_date': report.end_date,
            'total_actual_price_of_product': report.total_actual_price,
            'total_offer_discount': report.total_offer_discount
        }
        print('cotext done')

        # Generate and return the PDF
        
        pdf = render_to_pdf('salesreportpdf.html', context)
        print(pdf)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'
            return response
        return HttpResponse("Error generating PDF", status=500)
    return redirect(admin_login)
