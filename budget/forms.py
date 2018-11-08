from django import forms
from .models import BudgetCategory

class BudgetCategoryForm(forms.ModelForm):

    class Meta:
        model = BudgetCategory
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