from django.shortcuts import render
from .models import Budget
# Create your views here.

def budget_list(request):
    budgets = Budget.objects.filter(user=request.user).order_by('-created')
    context = {
        'budgets': budgets
    }
    return render(request, 'budget/budget_list.html', context)