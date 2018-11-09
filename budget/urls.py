from django.urls import path
from . import views

app_name='budget'

urlpatterns = [
    path('detail/', views.budget_detail, name='detail'),
    path('detail/<year>/<month>/', views.budget_detail, name='detail'),
    path('category/create/', views.budget_category_create, name='category_create'),
    path('category/<pk>/update/', views.BudgetCategoryUpdateView.as_view(), name='category_update'),
    path('category/<pk>/delete/', views.BudgetCategoryDeleteView.as_view(), name='category_delete'),
]
