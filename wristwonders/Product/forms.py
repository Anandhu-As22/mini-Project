from django.db import models
from django.forms import fields,ModelForm,inlineformset_factory
from .models import Category,Product,product_image,Brand
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator



class Add_category_form(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['category_name','description']
        widgets = {
            'category_name': forms.TextInput(attrs={
                'class': 'form-control ',
                'placeholder': 'Enter category name',
                'style': 'width: 100%; border: 2px solid #343A40; border-radius: 5px;',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control ',
                'placeholder': 'Enter description',
                'style': 'width: 100%; border: 2px solid #343A40; border-radius: 5px;',
                'rows': 4,
            }),
        }

class Update_form(forms.ModelForm):

    class Meta:
         model = Category
         fields = ['category_name','description']
         widgets = {
            'category_name': forms.TextInput(attrs={
                'class': 'form-control ',
                'placeholder': 'Enter category name',
                'style': 'width: 100%; border: 2px solid #343A40; border-radius: 5px;',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control ',
                'placeholder': 'Enter description',
                'style': 'width: 100%; border: 2px solid #343A40; border-radius: 5px;',
                'rows': 4,
            }),
        }



# product form


class Product_Form(ModelForm):
    
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),  # Ensure the field name matches the model
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'brand':forms.Select(attrs={'class':'form-control'})
        }

# class ProductVariant_Form(ModelForm):
#     class Meta:
#         model = ProductVarient
#         fields = ['colour', 'image']
#         widgets = {
#             'colour': forms.TextInput(attrs={'class': 'form-control'}),
#             'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
#         }

# ProductVariantFormSet = inlineformset_factory(Product, ProductVarient, form=ProductVariant_Form, extra=1,can_delete=True)
ProductImageFormSet = inlineformset_factory(Product, product_image, fields=['image'], extra=3,can_delete=True)



class Product_edit_form(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['Product_name','description','price','category','stock']
        widgets = {
            'Product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),  # Ensure the field name matches the model
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }
class Brand(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control',
                                           'placeholder': 'Enter brand name',
                'style': 'width: 100%; border: 2px solid #343A40; border-radius: 5px;',
                                           
                                           }),
        }