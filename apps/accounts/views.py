from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .forms import AccountForm
from .models import Account
from .serializers import AccountSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


@login_required
def wallets(request):
    accounts = request.user.accounts.all()
    context = {
        'accounts': accounts,
        "user": request.user,
    }
    return render(request, "wallets/wallets.html", context=context)


@login_required
def create_wallet(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            exists = Account.objects.filter(
                owner=request.user,
                type=form.cleaned_data['type'],
                currency=form.cleaned_data['currency']
            ).exists()
            if exists:
                messages.error(request, "Wallet with this type already exists.!")
                return render(request, "wallets/create_wallet.html", {"form": form})
            wallet = form.save(commit=False)
            wallet.owner = request.user
            wallet.save()
            return redirect('wallets:wallets')
    else:
        form = AccountForm()
    return render(request, "wallets/create_wallet.html", {"form": form})

@login_required
def delete_wallet(request, pk):
    wallet = get_object_or_404(Account, pk=pk, owner=request.user)
    if wallet.balance > 0:
        messages.error(request, "Cannot remove this wallet with positive balance!")
        return redirect('wallets:wallets')
    if request.method == "POST":
        wallet.delete()
        messages.success(request, "Current wallet is deleted!.")
        return redirect('wallets:wallets')
    return render(request, "wallets/confirm_delete_wallet.html", {"wallet": wallet})