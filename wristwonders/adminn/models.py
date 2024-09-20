from django.db import models
from django.utils import timezone
from Customers.models import User

# Create your models here.

class Coupon(models.Model):
    coupon_code = models.CharField(max_length=50)
    coupon_name = models.CharField()
    discount = models.DecimalField(max_digits=10,decimal_places=2)
    min_purchase_amount = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.coupon_name
    



class SalesReport(models.Model):
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_sales_delivered = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_order_count = models.IntegerField()
    coupon_discount = models.DecimalField(max_digits=10, decimal_places=2)
    total_actual_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_offer_discount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
