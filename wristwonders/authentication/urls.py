from django.urls import path
from . import views

urlpatterns =[
    path('user-login/',views.user_login,name='user-login'),
    path('user-signup/',views.user_signup,name='user-signup'),
    path('adminn/',views.admin_login,name='admin-login'),
    path('logout/',views.user_logout,name='user_logout')

]