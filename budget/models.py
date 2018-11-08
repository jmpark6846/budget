from django.contrib.auth.models import User
from django.db import models
from  functools import reduce


class BudgetCategory(models.Model):
    '''
    예산 항목. 예산 이름과 금액을 갖고 있다. 예) 이름: 교통비,  금액: 55000원
    '''
    name = models.CharField('예산', max_length=255)
    amount = models.IntegerField('금액')
    user = models.ForeignKey(User, related_name='categories',on_delete=models.CASCADE, verbose_name='사용자')
    created = models.DateTimeField('생성날짜', auto_now_add=True)
    updated = models.DateTimeField('수정날짜', auto_now=True)

    def __str__(self):
        return self.name


class Budget(models.Model):
    '''
    한 달치 예산. 년/월 정보 가진다.
    '''
    year = models.IntegerField('년')
    month = models.IntegerField('월')
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


    def budgeted(self):
        # 예산 잡힌 금액들. 한 달치 예산 항목들을 모두 더해 반환한다.
        return reduce(lambda sum, item: sum + item.category.amount, self.items.all(), 0)

    def spent_sum(self):
        return reduce(lambda sum, item: sum + item.spent, self.items.all(), 0)

    def __str__(self):
        return '{}월'.format(self.month)


class BudgetItem(models.Model):
    '''
    예산 항목. 예산 카테고리와 해당 예산으로 특정 월에 사용한 금액(spent)을 갖고 있다.
    '''
    category = models.ForeignKey(BudgetCategory, related_name='budget_items', on_delete=models.CASCADE, verbose_name='예산 카테고리')
    spent = models.IntegerField('금액', default=0)
    budget = models.ForeignKey(Budget, related_name='items', on_delete=models.CASCADE, verbose_name='예산')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.spent)

