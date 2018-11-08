from django.urls import path
from . import views

app_name='budget'

urlpatterns = [
    path('detail/', views.budget_detail, name='detail'),
    path('category/create/', views.budget_category_create, name='category_create'),
    path('category/<pk>/update/', views.BudgetCategoryUpdateView.as_view(), name='category_update'),
    # path('<pk>/delete/', views.BudgetDeleteView.as_view(), name='delete'),
]
