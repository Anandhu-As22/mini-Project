from django.urls import path
from . import views

urlpatterns =[
    path('adminn_home/',views.admin_home,name='admin-home'),
    path('adminn/user-list/',views.User_list,name ='adminn-user-list'),
    path('adminn/create-user/',views.add_user,name='adminn-add-user'),
    path('adminn/update-user/<pk>',views.Update_user,name='update-user'),
    path('adminn/unblock-user/<pk>',views.Un_block_user,name='unblock-user'),
    path('adminn/block-user/<pk>',views.block_user,name='block-user'),
    path('adminn/orders/',views.orders_list,name='adminnorders'),
    path('adminn/orderdetails/<int:pk>/',views.order_detail,name='adminnorderdetail'),
    path('adminn/coupons',views.coupon_list,name='coupon'),
    path('adminn/addcoupon',views.addcoupon,name='addcoupon'),
    path('adminn/editcoupon/<pk>',views.edit_coupon,name='editcoupon'),
    path('adminn/deletecopon/<pk>',views.deletecoupon,name='deletecoupon'),
     path('apply-coupon/',views.apply_coupon, name='apply_coupon'),
    



]