from django.contrib import admin
from .models import Cart,User_address,Cart_items,Wallet,Wishlist,Wishlist_items

# Register your models here.

admin.site.register(Cart)
admin.site.register(Cart_items)
admin.site.register(Wallet)
admin.site.register(Wishlist)
admin.site.register(Wishlist_items)
admin.site.register(User_address)

