from django import forms
from .models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'amount']
        widgets = {
            'name': forms.TextInput(attrs={
                'autocomplete': 'off',
                'placeholder': '계정 항목',
                'class': 'form-control',
            }),
            'amount': forms.NumberInput(attrs={
                'autocomplete': 'off',
                'placeholder': '금액',
                'class': 'form-control',
            })
        }