from django.contrib import admin
from .models import BudgetCategory, Budget, BudgetItem
# Register your models here.


admin.site.register(BudgetCategory)
admin.site.register(BudgetItem)
admin.site.register(Budget)