from django.urls import path
from . import views

app_name='account'

urlpatterns = [
    path('', views.account_list, name='list'),
    # path('create/', views.budget_create, name='create'),
    # path('<pk>/update/', views.BudgetUpdateView.as_view(), name='update'),
    # path('<pk>/delete/', views.BudgetDeleteView.as_view(), name='delete'),
]
