from django.contrib.auth.models import User
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