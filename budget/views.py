from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.utils import timezone
from django.http import HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from account.models import Account
from functools import reduce
from datetime import datetime
from .models import Budget, BudgetCategory, BudgetItem
from .forms import BudgetCategoryForm

now = timezone.now()

@login_required
def budget_detail(request, year=now.year, month=now.month):
    year_month = datetime.strptime('{}{}'.format(year,month), '%Y%m')
    budget, created = Budget.objects.get_or_create(year_month=year_month, user=request.user)

    request.session['budget_pk']=budget.pk
    accounts = Account.objects.filter(user=request.user)
    funds = reduce(lambda sum, acc: sum+acc.amount, accounts, 0)

    context = {
        'budget': budget,
        'funds': funds,
        'need_budgeted': funds - budget.budgeted_sum()
    }

    return render(request, 'budget/budget_detail.html', context)


@login_required
def budget_category_create(request):
    if request.method == 'POST':
        form = BudgetCategoryForm(request.POST)
        if form.is_valid():
            c = BudgetCategory(**form.cleaned_data)
            c.user = request.user
            c.save()

            if 'budget_pk' not in request.session:
                return HttpResponseBadRequest()

            budget = get_object_or_404(Budget, pk=request.session['budget_pk'])
            BudgetItem.objects.create(category=c, budget=budget)
            return redirect(reverse('budget:index'))
        else:
            context = { 'form': form }
            return render(request, 'budget/budget_category_form.html', context)
    else:
        form = BudgetCategoryForm()
        context = { 'form': form }
        return render(request, 'budget/budget_category_form.html', context)


class BudgetCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = BudgetCategory
    form_class = BudgetCategoryForm
    context_object_name = 'budget'
    template_name = 'budget/budget_category_form.html'

    def get_queryset(self):
        queryset = super(BudgetCategoryUpdateView, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('budget:index')


class BudgetCategoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = BudgetCategory
    success_url = reverse_lazy('budget:index')

    def get_queryset(self):
        queryset = super(BudgetCategoryDeleteView, self).get_queryset()
        return queryset.filter(user=self.request.user)
