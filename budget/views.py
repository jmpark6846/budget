from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.utils import timezone
from django.http import HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from account.models import Account
from functools import reduce
import datetime
from .models import Budget, BudgetCategory, BudgetItem
from .forms import BudgetCategoryForm

now = timezone.now()

# todo year, month를 year_month 객체 하나로 쓰기
@login_required
def budget_detail(request, year=now.year, month=now.month):
    _year, _month = int(year), int(month)

    if _month > 12:
        _year, _month = _year + 1, 1
    elif _month < 1:
        _year, _month = _year - 1, 12

    year_month = datetime.date(_year, _month, 1)
    budget, created = Budget.objects.get_or_create(year_month=year_month, user=request.user)

    request.session['budget_pk']=budget.pk
    accounts = Account.objects.filter(user=request.user)
    funds = reduce(lambda sum, acc: sum+acc.amount, accounts, 0)
    # budget_items = request.user.categories.budget_items.filter(budget=budget)

    category_budget_list = []

    for c in request.user.categories.order_by('-created'):
        i = c.budget_items.filter(budget=budget)[0]
        category_budget_list.append((c, i))

    context = {
        'budget': budget,
        'funds': funds,
        'category_budget_list': category_budget_list,
        'need_budgeted': funds - budget.budgeted_sum()
    }

    return render(request, 'budget/budget_detail.html', context)


@login_required
def budget_category_create(request, year, month):
    if request.method == 'POST':
        form = BudgetCategoryForm(request.POST)
        if form.is_valid():
            c = BudgetCategory(**form.cleaned_data)
            c.user = request.user
            c.save()

            _year, _month = int(year), int(month)

            if _month > 12 or _month < 1:
                return HttpResponseBadRequest()

            year_month = datetime.date(_year, _month, 1)
            budget, created = Budget.objects.get_or_create(year_month=year_month, user=request.user)

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
