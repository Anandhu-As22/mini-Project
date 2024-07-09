from django.urls import path
from . import views

urlpatterns =[
    path('category-list',views.Category_list,name='Category'),
    path('add-category',views.add_category,name='add-category'),
    path('edit-category/<pk>',views.edit_category,name='edit-category'),
    path('delete-category/<pk>',views.delete_category,name='delete-category'),
    path('undo-category/<pk>',views.undo_category,name='undo-category'),
    path('product-list/',views.Product_list,name='product-list'),
    path('add_product/',views.Add_product,name='add_product'),
    path('delete-product/<pk>',views.delete_product,name='delete-product'),
    path('softdelete-product/<pk>',views.soft_delete_product,name = 'softdelete-product'),
    path('edit-product/<pk>',views.update_product,name='update-product')

]