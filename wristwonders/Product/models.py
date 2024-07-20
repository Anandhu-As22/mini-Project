from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=250,unique=True)
    description = models.TextField()
    soft_delete = models.BooleanField(default=False)



    def __str__(self) -> str:
        return self.category_name
    


  
class Product(models.Model):
    Product_name = models.CharField(max_length=300,unique=True )
    description = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    price = models.FloatField()
    soft_delete = models.BooleanField(default=False)
    stock = models.PositiveIntegerField()


    def __str__(self) -> str:
        return self.Product_name
    

    
class product_image(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')

    image = models.FileField(upload_to='images')

    def __str__(self) -> str:
        return f"{self.product.Product_name} Image"
 

