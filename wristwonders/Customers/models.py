from django.db import models
from django.contrib.auth.models import AbstractUser
from Product.models import Product
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.utils import timezone
from Product.models import ProductOffer,Category_offer

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
        product_price = Decimal(self.product.price)  # Base price of the product

        # Check for category offer
        category_offer = Category_offer.objects.filter(
            category=self.product.category,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).first()

        # Check for product offer
        product_offer = ProductOffer.objects.filter(
            product=self.product,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).first()

        # Apply category and product offers
        if category_offer:
            category_product_price = product_price - (product_price * category_offer.discount_percentage / Decimal('100'))

        if product_offer:
            product_product_price = product_price - Decimal(product_offer.discount_price)

        # Determine the best price between category and product offer
        if category_offer and product_offer:
            product_price = min(category_product_price, product_product_price)
        elif category_offer:
            product_price = category_product_price
        elif product_offer:
            product_price = product_product_price

        # Return total price for the cart item
        return self.quantity * product_price
       
    

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user

class Wishlist_items(models.Model):
    wishlist = models.ForeignKey(Wishlist,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)


class Wallet(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)

    def __str__(self) -> str:
        return f"{self.user.username}'s Wallet - Balance: ${self.amount}"
    
    def credit(self,amount):
        self.amount += amount
        self.save()

    def debit(self,amount):
        if self.amount > amount:
            self.amount -= amount
            self.save()
            return True
        return False
    
class Transaction(models.Model):
    Transaction_types ={
        ('Credit','credit'),
        ('debit','Debit'),
        ('refund','Refund')

    }
    
    
    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10,choices=Transaction_types)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    Transaction_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.transaction_type.title()} - ${self.amount} - {self.Transaction_date.strftime('%Y-%m-%d %H:%M:%S')}"


    






