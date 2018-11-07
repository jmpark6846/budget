from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import generic
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from account.models import Account
from functools import reduce

from .models import Budget
from .forms import BudgetForm


@login_required
def budget_detail(request):
    year = request.GET.get('year', timezone.now().year)
    month = request.GET.get('month', timezone.now().month)
    budget, created = Budget.objects.get_or_create(year=year, month=month, user=request.user)


    accounts = Account.objects.filter(user=request.user)
    funds = reduce(lambda sum, acc: sum+acc.amount, accounts, 0)

    context = {
        'budget': budget,
        'funds': funds,
        'need_budgeted': funds - budget.budgeted()
    }
    return render(request, 'budget/budget_detail.html', context)


@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            todo = Budget(**form.cleaned_data)
            todo.user = request.user
            todo.save()
            return redirect(reverse('budget:list'))
        else:
            context = { 'form': form }
            return render(request, 'budget/budget_form.html', context)
    else:
        form = BudgetForm()
        context = { 'form': form }
        return render(request, 'budget/budget_form.html', context)



class BudgetUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Budget
    form_class = BudgetForm
    context_object_name = 'budget'
    template_name = 'budget/budget_form.html'

    def get_queryset(self):
        queryset = super(BudgetUpdateView, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('budget:list')


class BudgetDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Budget
    success_url = reverse_lazy('budget:list')

    def get_queryset(self):
        queryset = super(BudgetDeleteView, self).get_queryset()
        return queryset.filter(user=self.request.user)
