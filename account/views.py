from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Account

@login_required
def account_list(request):
    accounts = Account.objects.filter(user=request.user).order_by('-created')
    context = {
        'accounts': accounts
    }

    return render(request,'account/account_list.html', context)