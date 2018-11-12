from django.shortcuts import render, redirect, reverse, get_object_or_404
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


@login_required
def account_update(request, pk):
    account = get_object_or_404(Account, pk=pk)
    form = AccountForm(data=request.POST or None, instance=account)

    if form.is_valid():
        form.save()
        return redirect(reverse('account:list'))
    else:
        context = {'form': form}
        return render(request, 'account/account_form.html', context)


@login_required
def account_detail(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    context = { 'account': account }
    return render(request, 'account/account_detail.html', context)



@login_required
def account_delete(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)

    if request.method == 'POST':
        account.delete()
        return redirect(reverse('account:list'))
    else:
        context = { 'account': account }
        return render(request, 'account/account_confirm_delete.html', context)