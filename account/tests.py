from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Account

class AccountModelTestCase(TestCase):
    def create_user(self, name, pw):
        user = User.objects.create(username=name)
        user.set_password(pw)
        user.save()
        return user

    def setUp(self):
        self.user = self.create_user('tom', '12345')
        self.client.login(username='tom', password='12345')

    def test_model_can_create_an_account(self):
        old_count = Account.objects.count()
        Account.objects.create(name='교통비', amount=55000, user=self.user)
        new_count = Account.objects.count()
        self.assertNotEqual(old_count, new_count)


class AccountViewTestCase(TestCase):
    def create_user(self, name, pw):
        user = User.objects.create(username=name)
        user.set_password(pw)
        user.save()
        return user

    def setUp(self):
        self.user = self.create_user('tom', '12345')
        self.client.login(username='tom', password='12345')
        self.account = Account.objects.create(name='체크카드', amount='1000', user=self.user)

    def test_view_can_list_accounts(self):
        for i in range(0,5):
            Account.objects.create(name="test account name #{}".format(i), amount=i, user=self.user)

        res = self.client.get(reverse('account:list'))
        self.assertEqual(res.status_code, 200)


    def test_view_can_create_accounts(self):
        account_data = {
            'name': '체크카드',
            'amount': 5000,
        }
        res = self.client.post(reverse('account:create'), account_data)
        self.assertEqual(res.status_code, 302)


    def test_view_can_show_account_detail(self):
        res = self.client.get(reverse('account:detail', kwargs={'pk': self.account.pk}))
        self.assertEqual(res.status_code,200)