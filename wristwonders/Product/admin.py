
from django.contrib import admin
from .models import Product, product_image

# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = product_image
    extra = 3

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)
