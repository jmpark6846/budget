from django.contrib.auth.models import User
from django.db import models

class BudgetCategory(models.Model):
    name = models.CharField('예산', max_length=255)
    amount = models.IntegerField('금액')
    user = models.ForeignKey(User, related_name='budgets',on_delete=models.CASCADE, verbose_name='사용자')
    created = models.DateTimeField('생성날짜', auto_now_add=True)
    updated = models.DateTimeField('수정날짜', auto_now=True)

    def __str__(self):
        return self.name


class BudgetItem(models.Model):
    category = models.ForeignKey(BudgetCategory, related_name='budget_items', on_delete=models.CASCADE, verbose_name='예산 카테고리')
    amount_in_budget = models.IntegerField('금액')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.amount_in_budget)


class Budget(models.Model):
    month = models.DateField('월')
    items = models.ManyToManyField(BudgetItem, related_name= 'budgets')

    def __str__(self):
        return self.month

