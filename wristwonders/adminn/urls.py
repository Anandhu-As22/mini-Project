from django.urls import path
from . import views

urlpatterns =[
    path('adminn_home/',views.admin_home,name='admin-home'),
    path('adminn/user-list/',views.User_list,name ='adminn-user-list'),
    path('adminn/create-user/',views.add_user,name='adminn-add-user'),
    path('adminn/update-user/<pk>',views.Update_user,name='update-user'),
    path('adminn/unblock-user/<pk>',views.Un_block_user,name='unblock-user'),
    path('adminn/block-user/<pk>',views.block_user,name='block-user'),



]