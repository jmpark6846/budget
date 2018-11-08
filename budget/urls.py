from django.urls import path
from . import views

app_name='budget'

urlpatterns = [
    # path('create/', views.budget_create, name='create'),
    path('detail/', views.budget_detail, name='detail'),
    # path('<pk>/update/', views.BudgetUpdateView.as_view(), name='update'),
    # path('<pk>/delete/', views.BudgetDeleteView.as_view(), name='delete'),
]
