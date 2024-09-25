
from django.contrib import admin
from .models import Product, product_image,Category,Category_offer,Brand,ProductOffer

# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = product_image
    extra = 3

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)

admin.site.register(Brand)
admin.site.register(Category_offer)
admin.site.register(ProductOffer)
