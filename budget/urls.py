from django.urls import path
from . import views

app_name='budget'

urlpatterns = [
  path('', views.budget_list, name='list'),
  path('create/', views.budget_create, name='create'),
]
