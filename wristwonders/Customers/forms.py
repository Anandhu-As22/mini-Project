from django import forms
from django.db import models
from django.forms import ModelForm
from .models import User_address,User

class addaddressform(forms.ModelForm):
    class Meta:
        model = User_address
        fields = ['house_name', 'street','city', 'district', 'state', 'pincode', 'phone_no']
        widgets = {
            'house_name': forms.TextInput(attrs={'placeholder': 'Enter house_no','class':'form-control'}),
            'street': forms.TextInput(attrs={'placeholder': 'Enter street addrees','class':'form-control'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter city','class':'form-control'}),
            'district': forms.TextInput(attrs={'placeholder': 'Enter district','class':'form-control'}),
            'state': forms.TextInput(attrs={'placeholder': 'Enter state','class':'form-control'}),
            'pincode': forms.TextInput(attrs={'placeholder': 'Enter pincode','class':'form-control'}),
            'phone_no': forms.TextInput(attrs={'placeholder': 'Enter phone number','class':'form-control'}),
        }

class editaddressform(ModelForm):
    class Meta:
        model = User_address
        fields = ['house_name','street','city','district','state','pincode','phone_no']
        widgets = {
            'house_name': forms.TextInput(attrs={'placeholder': 'Enter house_no','class':'form-control'}),
            'street': forms.TextInput(attrs={'placeholder': 'Enter street addrees','class':'form-control'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter city','class':'form-control'}),
            'district': forms.TextInput(attrs={'placeholder': 'Enter district','class':'form-control'}),
            'state': forms.TextInput(attrs={'placeholder': 'Enter state','class':'form-control'}),
            'pincode': forms.TextInput(attrs={'placeholder': 'Enter pincode','class':'form-control'}),
            'phone_no': forms.TextInput(attrs={'placeholder': 'Enter phone number','class':'form-control'}),
        }
        
class edituserform(ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        widgets ={
            'username' : forms.TextInput(attrs={'placeholder':'username','class':'form-control'}),
            'first_name' : forms.TextInput(attrs={'placeholder':'first_name','class':'form-control'}),
            'last_name' : forms.TextInput(attrs={'placeholder':'last_name','class':'form-control'}),
            'email' : forms.EmailInput(attrs={'placeholder':'email','class':'form-control'})
        }