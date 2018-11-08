from django.contrib.auth.models import User
from django.utils import timezone

from django.db import models
from  functools import reduce


class BudgetCategory(models.Model):
    '''
    예산 항목.
    '''
    name = models.CharField('예산', max_length=255)
    user = models.ForeignKey(User, related_name='categories',on_delete=models.CASCADE, verbose_name='사용자')
    created = models.DateTimeField('생성날짜', auto_now_add=True)
    updated = models.DateTimeField('수정날짜', auto_now=True)

    def __str__(self):
        return self.name


class Budget(models.Model):
    '''
    한 달치 예산. 년/월 정보 가진다.
    '''
    year = models.IntegerField('년', default=timezone.now().year)
    month = models.IntegerField('월', default=timezone.now().month)
    user = models.ForeignKey(User, related_name='budgets',on_delete=models.CASCADE, verbose_name='사용자')

    def save(self, *args, **kwargs):
        created = False
        if not self.pk:
            created=True

        super(Budget, self).save(*args, **kwargs)

        if created:
            # 예산 생성 시 카테고리 전부 들고오기 -> 항목 생성 -> 예산에 추가
            categories = BudgetCategory.objects.filter(user=self.user)

            for c in categories:
                item = BudgetItem.objects.create(category=c, budget=self)
                self.items.add(item)

            self.save()


    def budgeted_sum(self):
        # 예산 잡힌 금액들. 한 달치 예산 항목들을 모두 더해 반환한다.
        return reduce(lambda sum, item: sum + item.budgeted, self.items.all(), 0)

    def activity_sum(self):
        return reduce(lambda sum, item: sum + item.activity, self.items.all(), 0)

    def __str__(self):
        return '{}월'.format(self.month)


class BudgetItem(models.Model):
    '''
    예산 항목.
    '''
    category = models.ForeignKey(BudgetCategory, related_name='budget_items', on_delete=models.CASCADE, verbose_name='예산 카테고리')
    budgeted = models.IntegerField('예산 금액', default=0)
    activity = models.IntegerField('사용 금액', default=0)
    budget = models.ForeignKey(Budget, related_name='items', on_delete=models.CASCADE, verbose_name='예산')

    def __str__(self):
        return '{} : {} / {}'.format(self.category.name, self.activity, self.budgeted)

