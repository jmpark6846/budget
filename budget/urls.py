from django.urls import path
from . import views

app_name='budget'

urlpatterns = [
    path('', views.budget_detail, name='index'),
    path('detail/<year_month>/', views.budget_detail, name='detail'),
    path('detail/<year_month>/category/create/', views.budget_category_create, name='category_create'),
    path('category/<pk>/update/', views.BudgetCategoryUpdateView.as_view(), name='category_update'),
    path('category/<pk>/delete/', views.BudgetCategoryDeleteView.as_view(), name='category_delete'),
    path('item/<pk>/update/', views.BudgetItemUpdateView.as_view(), name='item_update'),
    path('<year_month>/category/<category_pk>/item/create', views.budget_items_create, name='item_create'),
]
