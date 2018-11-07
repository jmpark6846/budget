from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import generic
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from account.models import Account
from .models import Budget
from .forms import BudgetForm
from functools import reduce


@login_required
def budget_detail(request, year=timezone.now().year, month=timezone.now().month):
    budget = Budget.objects.get_or_create(year=year, month=month, user=request.user)

    context={ 'budget':budget }

    # accounts = Account.objects.filter(user=request.user)
    # funds = reduce(lambda sum, acc: sum+acc.amount, accounts, 0)
    # budgeted = reduce(lambda sum, bdg: sum+bdg.amount, budget, 0)
    #
    # context = {
    #     'budgets': budgets,
    #     'funds': funds,
    #     'budgeted': budgeted,
    #     'need_budgeted': funds - budgeted
    # }
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
