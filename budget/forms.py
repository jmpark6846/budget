from django import forms
from .models import BudgetCategory, BudgetItem

class BudgetCategoryForm(forms.ModelForm):

    class Meta:
        model = BudgetCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'autocomplete': 'off',
                'placeholder': '예산 항목',
                'class': 'form-control',
            }),
        }

class BudgetItemForm(forms.ModelForm):

    class Meta:
        model = BudgetItem
        fields = ['budgeted']
        widgets = {
            'budgeted': forms.TextInput(attrs={
                'autocomplete': 'off',
                'placeholder': '예산 금액',
                'class': 'form-control',
            }),
        }