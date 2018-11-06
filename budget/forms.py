from django import forms
from .models import Budget

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'amount']
        widgets = {
            'name': forms.TextInput(attrs={
                'autocomplete': 'off',
                'placeholder': '예산 항목',
                'class': 'form-control',
            }),
            'amount': forms.NumberInput(attrs={
                'autocomplete': 'off',
                'placeholder': '금액',
                'class': 'form-control',
            })
        }