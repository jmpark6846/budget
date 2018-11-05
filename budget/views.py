from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import Budget
from .forms import BudgetForm
# Create your views here.

@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user).order_by('-created')
    context = {
        'budgets': budgets
    }
    return render(request, 'budget/budget_list.html', context)

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
