from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
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
