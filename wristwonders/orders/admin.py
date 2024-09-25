from django.contrib import admin

from .models import Order,Order_cancellation,Order_item,return_reason


# Register your models here.

admin.site.register(Order)
admin.site.register(Order_cancellation)
admin.site.register(Order_item)
admin.site.register(return_reason)
