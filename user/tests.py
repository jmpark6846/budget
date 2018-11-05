from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.conf import settings


class UserViewTest(TestCase):
  def setUp(self):
    user = User.objects.create(username='tom')
    user.set_password('12345')
    user.save()
    self.user = user

  def test_login_with_created_user(self):
    user_data = { "username": "tom", "password": "12345" }
    res = self.client.post(reverse('user:login'), data=user_data)

    self.assertEqual(res.url, settings.LOGIN_REDIRECT_URL)
    self.assertEqual(res.status_code, 302) # redirect after login
  
  def test_logout(self):
    self.client.login(username='tom', password='12345')
    res = self.client.get(reverse('user:logout'))

    self.assertEqual(res.url, settings.LOGOUT_REDIRECT_URL)
    self.assertEqual(res.status_code, 302) # redirect after logout

  def test_create_user_with_signup_view(self):
    user_data={ "username": "john", "password1": "123abc!@#", "password2": "123abc!@#"}
    res = self.client.post(reverse('user:signup'), data=user_data)
    self.assertEqual(res.context['user'].username, "john")
    self.assertEqual(res.status_code, 200)


