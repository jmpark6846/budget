from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': '아이디',
                'class': 'form-control',
            }),
            'password': forms.TextInput(attrs={
                'placeholder': '패스워드',
                'class': 'form-control',
            }),
        }


class SignupForm(UserCreationForm):
    class Meta:
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': '아이디',
                'class': 'form-control',
            }),
            'password': forms.TextInput(attrs={
                'placeholder': '패스워드',
                'class': 'form-control',
            }),
        }
