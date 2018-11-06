from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    name = models.CharField('계정 이름', max_length=255)
    amount = models.IntegerField('금액')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts', verbose_name='사용자')
    created = models.DateTimeField('생성날짜', auto_now_add=True)
    updated = models.DateTimeField('수정날짜', auto_now=True)

    def __str__(self):
        return '{}의 계정: {}'.format(self.user.username, self.name)

