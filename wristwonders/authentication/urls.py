from django.urls import path
from . import views

urlpatterns =[
    path('user-login/',views.user_login,name='user-login'),
    path('user-signup/',views.user_signup,name='user-signup'),
    path('adminn/',views.admin_login,name='admin-login'),
    path('adminn/logout',views.adminn_logout,name = 'adminn-logout'),
    path('logout/',views.user_logout,name='user_logout'),
    path('otp-verification/',views.otp_verification,name='otp-verification'),
    path('resend-otp/',views.resend_otp,name='resend-otp')



]