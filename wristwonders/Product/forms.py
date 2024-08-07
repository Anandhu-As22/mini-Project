from django.db import models
from django.forms import fields,ModelForm,inlineformset_factory
from .models import Category,Product,product_image
from django import forms



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
        }

# class Product_Image_Form(forms.ModelForm):
#     class Meta:
        
#         model = product_image
#         fields = ['image']

ProductImageFormSet = inlineformset_factory(Product, product_image, form=forms.ModelForm, fields=['image'], extra=3)