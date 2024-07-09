from django.db import models
from django.contrib.auth.models import AbstractUser
from Product.models import Product
from django.core.validators import RegexValidator
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(max_length=300,unique=True)


class User_address(models.Model):
    customers = models.ForeignKey(User, on_delete=models.CASCADE)
    house_name = models.CharField(max_length=255)  # Add max_length
    street = models.CharField(max_length=255) 
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)  # Use CharField for flexibility

    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be 10 digits long."
    )
    phone_no = models.CharField(
        validators=[phone_regex],
        max_length=10,
        default='1234567890'  # Ensure default is a string
    )

class Cart(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)



class Cart_items(models.Model):
    cart= models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total(self):
        return self.quantity * self.product.price
    




