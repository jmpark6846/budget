from django.urls import path
from . import views

app_name='account'

urlpatterns = [
    path('', views.account_list, name='list'),
    path('create/', views.AccountCreateView.as_view(), name='create'),
    path('<pk>/detail/', views.account_detail, name='detail'),
    path('<pk>/delete/', views.account_delete, name='delete'),
    path('<pk>/update/', views.account_update, name='update'),
]
