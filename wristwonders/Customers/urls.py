from django.urls import path
from . import views

urlpatterns =[
    path('',views.index_page,name ='index' ),
    path('home',views.Home_page,name ='home' ),
    path('product-detail/<int:pk>/',views.product_detail,name='product-detail' ),
    path('user-profile/<int:pk>/',views.user_profile,name='userprofile'),
    path('cart/',views.view_cart,name='view-cart'),
    path('add-to-cart/<int:pk>/',views.add_to_cart,name='add-cart'),
    path('remove_cart/<int:pk>/',views.remove_cart, name='remove_cart'),
    path('update_cart/<int:pk>/',views.update_cart,name='update-cart'),
    path('add-address/',views.add_address,name='add-address'),
    path('edit-address/<int:pk>/',views.editaddress,name='edit-address'),
    path('delete-address/<int:pk>/',views.delete_address,name='delete-address'),
    path('checkout/',views.Checkout,name='checkout'),
    path('allproducts/',views.all_products,name='allproducts'),
    path('user-order-details/<int:pk>/',views.user_order_details,name='userorderdetails'),
    path('wishlist/',views.wish_list,name='wishlist'),
    path('add-wishlist/<int:pk>/',views.add_wishlist,name='add-wishlist'),
    path('remove-wishlist/<int:pk>/',views.remove_wishlist,name='remove-wishlist')


]   