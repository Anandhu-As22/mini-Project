from django.urls import path
from . import views

urlpatterns =[
    path('',views.index_page,name ='index' ),
    path('home',views.Home_page,name ='home' ),
    path('product-detail/<int:pk>/',views.product_detail,name='product-detail' ),
]