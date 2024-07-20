from django import forms
from Customers.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Coupon


class UpdateForm(ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    is_staff = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'is_staff']



class AddCouponForm(ModelForm):
    class Meta:
        model=Coupon
        fields=['coupon_code','coupon_name','discount','min_purchase_amount','is_active']

class EditCouponForm(ModelForm):
    class Meta:
        model =Coupon
        fields='__all__'  
        exclude = ['created_at'] 



