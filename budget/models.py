from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Budget(models.Model):
    name = models.CharField('예산', max_length=255)
    amount = models.IntegerField('금액')
    user = models.ForeignKey(User, related_name='budgets',on_delete=models.CASCADE, verbose_name='사용자')
    created = models.DateTimeField('생성날짜', auto_now_add=True)
    updated = models.DateTimeField('수정날짜', auto_now=True)

    def __str__(self):
        return self.name
