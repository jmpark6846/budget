from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .models import BudgetCategory

# Create your tests here.
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
        BudgetCategory.objects.create(name='교통비', amount=55000, user=self.user)
        new_count = BudgetCategory.objects.count()
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


#
#
# class BudgetCategoryViewTestCase(TestCase):
#     def create_user(self, name, pw):
#         user = User.objects.create(username=name)
#         user.set_password(pw)
#         user.save()
#         return user
#
#     def setUp(self):
#         self.user = self.create_user('tom', '12345')
#         self.client.login(username='tom', password='12345')
#         self.budget_category = BudgetCategory.objects.create(name="test budget_category", amount=1000, user=self.user)
#
#     def test_view_can_list_budget_categorys(self):
#         for i in range(0,5):
#             BudgetCategory.objects.create(name="test budget_category name #{}".format(i), amount=i, user=self.user)
#
#         res = self.client.get(reverse('budget_category:list'))
#         self.assertEqual(res.status_code, 200)
#
#     def test_view_can_create_budget_category(self):
#         budget_category_data = { 'name': '교통', 'amount': 1000, 'user': self.user}
#         res = self.client.post(reverse('budget_category:create'), budget_category_data)
#         self.assertEqual(res.status_code, 302)  # 생성 성공시 리다이렉트
#
#     def test_view_can_update_budget_category(self):
#         budget_category_data = {'name': '교통', 'amount': 1000, 'user': self.user}
#         res = self.client.post(reverse('budget_category:update', kwargs={'pk': self.budget_category.pk}), budget_category_data)
#         self.assertEqual(res.status_code, 302)
#
#     def test_view_can_delete_budget_category(self):
#         old_count = BudgetCategory.objects.count()
#         self.client.delete(reverse('budget_category:delete', kwargs={'pk': self.budget_category.pk}))
#         new_count = BudgetCategory.objects.count()
#         self.assertNotEqual(old_count, new_count)