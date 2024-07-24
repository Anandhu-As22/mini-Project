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
    

    path('category-offers/',views.categoryoffers,name="category-offers"),
    path('add-category-offer/', views.add_category_offer, name='add-category-offer'),
    path('edit-category-offer/<pk>',views.editCategoryOffer,name='edit-category-offer'),
    path('delete-categoryoffer/<pk>',views.deleteCategoryOffer,name="delete-categoryoffer"),
    

    path('product-offers/',views.productoffers,name="product-offers"),
    path('add-product-offer/', views.add_product_offer, name='add-product-offer'),
    path('edit-product-offers/<pk>',views.editProductOffers,name="edit-product-offers"),
    path('delete-productoffer/<pk>',views.deleteProductOffer,name="delete-productoffer"),
    



]