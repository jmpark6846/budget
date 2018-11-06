from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .models import Budget

# Create your tests here.
class BudgetModelTestCase(TestCase):
    def create_user(self, name, pw):
        user = User.objects.create(username=name)
        user.set_password(pw)
        user.save()
        return user

    def setUp(self):
        self.user = self.create_user('tom', '12345')
        self.client.login(username='tom', password='12345')

    def test_model_can_create_a_budget(self):
        old_count = Budget.objects.count()
        Budget.objects.create(name='교통비', amount=55000, user=self.user)
        new_count = Budget.objects.count()
        self.assertNotEqual(old_count, new_count)


class BudgetViewTestCase(TestCase):
    def create_user(self, name, pw):
        user = User.objects.create(username=name)
        user.set_password(pw)
        user.save()
        return user

    def setUp(self):
        self.user = self.create_user('tom', '12345')
        self.client.login(username='tom', password='12345')
        self.budget = Budget.objects.create(name="test budget", amount=1000, user=self.user)

    def test_view_can_list_budgets(self):
        for i in range(0,5):
            Budget.objects.create(name="test budget name #{}".format(i), amount=i, user=self.user)

        res = self.client.get(reverse('budget:list'))
        self.assertEqual(res.status_code, 200)

    def test_view_can_create_budget(self):
        budget_data = { 'name': '교통', 'amount': 1000, 'user': self.user}
        res = self.client.post(reverse('budget:create'), budget_data)
        self.assertEqual(res.status_code, 302)  # 생성 성공시 리다이렉트

    def test_view_can_update_budget(self):
        budget_data = {'name': '교통', 'amount': 1000, 'user': self.user}
        res = self.client.post(reverse('budget:update', kwargs={'pk': self.budget.pk}), budget_data)
        self.assertEqual(res.status_code, 302)

    def test_view_can_delete_budget(self):
        old_count = Budget.objects.count()
        self.client.delete(reverse('budget:delete', kwargs={'pk': self.budget.pk}))
        new_count = Budget.objects.count()
        self.assertNotEqual(old_count, new_count)