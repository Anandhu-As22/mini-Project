from django.urls import path
from . import views


urlpatterns = [
    path('order-success/',views.Order_success,name='order-success'),
    path('order-cancel/<pk>',views.ordercancel,name='ordercancel'),
    
    path('return-order/<pk>',views.returnrequest,name='returnrequest'),
    path('onlinepayment',views.paymenthomepage,name='paymenthome'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),



    path('order-dettail-pdf/<int:pk>',views.order_pdf_view,name='order-pdf')
]