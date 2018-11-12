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
from dateutil import relativedelta
from .models import Budget, BudgetCategory, BudgetItem
from .forms import BudgetCategoryForm, BudgetItemForm

now = timezone.now().strftime('%Y%m')

@login_required
def budget_detail(request, year_month=now):
    _year_month = datetime.strptime(year_month, '%Y%m')
    budget, created = Budget.objects.get_or_create(year_month=_year_month, user=request.user)

    request.session['budget_pk']=budget.pk
    accounts = Account.objects.filter(user=request.user)
    funds = reduce(lambda sum, acc: sum+acc.amount, accounts, 0)
    # budget_items = request.user.categories.budget_items.filter(budget=budget)

    category_budget_list = []

    for c in request.user.categories.order_by('-created'):
        filtered = c.budget_items.filter(budget=budget)
        i = filtered[0] if filtered.count() else None
        category_budget_list.append((c, i))

    context = {
        'budget': budget,
        'funds': funds,
        'category_budget_list': category_budget_list,
        'need_budgeted': funds - budget.budgeted_sum(),
        'next_month': _year_month + relativedelta.relativedelta(months=1),
        'prev_month': _year_month - relativedelta.relativedelta(months=1)
    }
    return render(request, 'budget/budget_detail.html', context)


@login_required
def budget_category_create(request, year_month):
    if request.method == 'POST':
        form = BudgetCategoryForm(request.POST)
        if form.is_valid():
            c = BudgetCategory(**form.cleaned_data)
            c.user = request.user
            c.save()

            _year_month = datetime.strptime(year_month, '%Y%m')
            budget, created = Budget.objects.get_or_create(year_month=_year_month, user=request.user)

            BudgetItem.objects.create(category=c, budget=budget)
            return redirect(reverse('budget:index'))
        else:
            context = { 'form': form }
            return render(request, 'budget/budget_category_form.html', context)
    else:
        form = BudgetCategoryForm()
        context = { 'form': form }
        return render(request, 'budget/budget_category_form.html', context)



@login_required
def budget_items_create(request, year_month, category_pk):
    _year_month = datetime.strptime(year_month, '%Y%m')
    if request.method == 'POST':
        form = BudgetItemForm(request.POST)
        if form.is_valid():
            budget = get_object_or_404(Budget, year_month=_year_month, user=request.user)
            category = get_object_or_404(BudgetCategory, pk=category_pk, user=request.user)
            item = BudgetItem(budget=budget, category=category, budgeted=form.cleaned_data['budgeted'])
            item.save()
            return redirect(reverse('budget:detail', kwargs={'year_month':_year_month}))
        else:
            return render(request, 'budget/budget_item_form.html', {'form': form})
    else:
        form = BudgetItemForm()
        return render(request, 'budget/budget_item_form.html', {'form':form})


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


class BudgetItemUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = BudgetItem
    form_class = BudgetItemForm
    context_object_name = 'budget_item'
    template_name = 'budget/budget_item_form.html'

    def get_queryset(self):
        queryset = super(BudgetItemUpdateView, self).get_queryset()
        return queryset.filter(budget__user=self.request.user)

    def get_success_url(self):
        return reverse('budget:detail', kwargs={'year_month':self.object.budget.year_month.strftime('%Y%m')})