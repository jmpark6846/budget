from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import views, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import LoginForm

class LoginView(views.LoginView):
  template_name = 'user/login.html'


def signup(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect(reverse('todo:list'))
    else:
      return render(request, 'user/signup.html', { 'form': form })
  else:
    form = UserCreationForm()
    return render(request, 'user/signup.html', { 'form': form })
