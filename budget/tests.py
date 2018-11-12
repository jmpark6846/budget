from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .models import BudgetCategory, Budget, BudgetItem

# Create your tests here.

def create_user(name, pw):
    user = User.objects.create(username=name)
    user.set_password(pw)
    user.save()
    return user

class BudgetCategoryModelTestCase(TestCase):
    def create_user(self, name, pw):
        user = User.objects.create(username=name)
        user.set_password(pw)
        user.save()
        return user

    def setUp(self):
        self.user = self.create_user('tom', '12345')
        self.client.login(username='tom', password='12345')

    def test_model_can_create_a_budget_category(self):
        old_count = BudgetCategory.objects.count()
        BudgetCategory.objects.create(name='교통비', user=self.user)
        new_count = BudgetCategory.objects.count()
        self.assertNotEqual(old_count, new_count)


class BudgetModelTestCase(TestCase):
    def setUp(self):
        self.user = create_user('tom', '12345')
        self.client.login(username='tom', password='12345')
        BudgetCategory.objects.create(name='교통', user=self.user)
        BudgetCategory.objects.create(name='생활', user=self.user)
        year_month = datetime.strptime('201809', '%Y%m')
        self.budget = Budget.objects.create(year_month=year_month, user=self.user)

    def test_model_can_get_budgeted_sum(self):
        self.assertEqual(self.budget.budgeted_sum(), 0)

        for item in self.budget.items.all():
            item.budgeted=2000
            item.save()

        self.assertEqual(self.budget.budgeted_sum(), 4000)

    def test_can_add_items_when_create_budget(self):
        self.assertEqual(self.budget.items.count(), 2)


class BudgetViewTestCase(TestCase):
    def create_user(self, name, pw):
        user = User.objects.create(username=name)
        user.set_password(pw)
        user.save()
        return user

    def setUp(self):
        self.user = self.create_user('tom', '12345')
        self.client.login(username='tom', password='12345')
        category = BudgetCategory.objects.create(name='교통비', user=self.user)
        BudgetItem.objects.create(category=category, budgeted=70000)
        self.budget=Budget.objects.create(user=self.user)


    def view_can_show_a_budget_this_month(self):
        res = self.client.get(reverse('budget:index'))
        self.assertEqual(res.status_code, 200)

    def can_show_a_budget_other_month(self):
        res = self.client.get(reverse('budget:detail', kwargs={ 'year': 2018, 'month': 5 }))
        self.assertEqual(res.context['budget'].year_month.month, 5)


class BudgetCategoryViewTestCase(TestCase):
    def create_user(self, name, pw):
        user = User.objects.create(username=name)
        user.set_password(pw)
        user.save()
        return user

    def setUp(self):
        self.user = self.create_user('tom', '12345')
        self.client.login(username='tom', password='12345')
        self.budget_category = BudgetCategory.objects.create(name="test budget_category", user=self.user)
        self.budget = Budget.objects.create(user=self.user)
        session = self.client.session
        session['budget_pk'] = self.budget.pk
        session.save()

    def test_view_can_create_budget_category(self):
        budget_category_data = { 'name': '교통', 'user': self.user}
        res = self.client.post(reverse('budget:category_create', kwargs={'year_month':self.budget.year_month.strftime('%Y%m')}), budget_category_data)
        self.assertEqual(res.status_code, 302)  # 생성 성공시 리다이렉트

    def test_view_can_update_budget_category(self):
        budget_category_data = {'name': '교통', 'user': self.user}
        res = self.client.post(reverse('budget:category_update', kwargs={'pk': self.budget_category.pk}), budget_category_data)
        self.assertEqual(res.status_code, 302)

    def test_view_can_delete_budget_category(self):
        old_count = BudgetCategory.objects.count()
        self.client.delete(reverse('budget:category_delete', kwargs={'pk': self.budget_category.pk}))
        new_count = BudgetCategory.objects.count()
        self.assertNotEqual(old_count, new_count)