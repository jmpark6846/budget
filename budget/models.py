from django.contrib.auth.models import User
from django.db import models
from  functools import reduce


class BudgetCategory(models.Model):
    name = models.CharField('예산', max_length=255)
    amount = models.IntegerField('금액')
    user = models.ForeignKey(User, related_name='categories',on_delete=models.CASCADE, verbose_name='사용자')
    created = models.DateTimeField('생성날짜', auto_now_add=True)
    updated = models.DateTimeField('수정날짜', auto_now=True)

    def __str__(self):
        return self.name


class BudgetItem(models.Model):
    category = models.ForeignKey(BudgetCategory, related_name='budget_items', on_delete=models.CASCADE, verbose_name='예산 카테고리')
    amount_in_budget = models.IntegerField('금액')

    def save(self, *args, **kwargs):
        # 예산 항목 생성 시 금액을 설정하지 않으면 카테고리의 금액을 기본값으로 입력
        if not self.amount_in_budget:
            self.amount_in_budget = self.category.amount

        super(BudgetItem, self).save(*args, **kwargs)

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.amount_in_budget)


class Budget(models.Model):
    year = models.IntegerField('년')
    month = models.IntegerField('월')

    items = models.ManyToManyField(BudgetItem, related_name= 'budgets')
    user = models.ForeignKey(User, related_name='budgets',on_delete=models.CASCADE, verbose_name='사용자')

    def budgeted(self):
        return reduce(lambda sum, item: sum + item.amount_in_budget, self.items.all(), 0)

    def __str__(self):
        return '{}월'.format(self.month)

