from django.urls import path
from . import views


urlpatterns = [
    path('order-success/',views.Order_success,name='order-success'),
    path('order-cancel/<pk>',views.ordercancel,name='ordercancel'),
    path('return-order/<pk>',views.returnrequest,name='returnrequest')
]