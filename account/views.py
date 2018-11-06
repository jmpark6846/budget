from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Account
from .forms import AccountForm

@login_required
def account_list(request):
    accounts = Account.objects.filter(user=request.user).order_by('-created')
    context = {
        'accounts': accounts
    }

    return render(request,'account/account_list.html', context)


class AccountCreateView(generic.CreateView):
    model = Account
    template_name = 'account/account_form.html'
    form_class = AccountForm
    success_url = reverse_lazy('account:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AccountCreateView, self).form_valid(form)

