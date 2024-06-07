from Customers.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length =260,widget=forms.TextInput(attrs={'class':'form-control w-50','placeholder':'username'}))
    password = forms.CharField( widget=forms.PasswordInput(attrs={'class':'form-control w-50 ','placeholder':'password'}))


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=300, required=True)
    first_name = forms.CharField(max_length=300, required=True)
    last_name = forms.CharField(max_length=300, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control w-50'})
        self.fields['username'].widget.attrs.update({'class': 'form-control w-50'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control w-50'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control w-50'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control w-50'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control w-50'})
