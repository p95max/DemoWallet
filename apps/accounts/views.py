from decimal import Decimal

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from django.db.models import Q, Prefetch

from config import settings
from .forms import AccountForm, TopUpForm, TransferForm
from .models import Account
from apps.transactions.models import Transaction
from .serializers import AccountSerializer
from django.contrib.auth.decorators import login_required

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.select_related('owner').all()
    serializer_class = AccountSerializer

@login_required
def wallets(request):
    transaction_fields = ['id', 'amount', 'txn_type', 'created_at', 'account_from_id', 'account_to_id', 'currency']
    accounts = (
        request.user.accounts
        .select_related('owner')
        .prefetch_related(
            Prefetch('incoming_transactions', queryset=Transaction.objects.only(*transaction_fields)),
            Prefetch('outgoing_transactions', queryset=Transaction.objects.only(*transaction_fields)),
        )
        .all()
    )
    context = {
        'accounts': accounts,
        "user": request.user,
    }
    return render(request, "wallets/wallets.html", context=context)

@login_required
def wallet_detail(request, pk):
    wallet = get_object_or_404(
        Account.objects.select_related('owner'),
        pk=pk, owner=request.user
    )
    transactions = (
        Transaction.objects
        .filter(Q(account_from=wallet) | Q(account_to=wallet))
        .select_related('account_from', 'account_to')
        .order_by('-created_at')
    )
    context = {
        "wallet": wallet,
        "transactions": transactions,
    }
    return render(request, "wallets/wallet_detail.html", context=context)

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
                messages.error(request, "Wallet with this type already exists!")
                return render(request, "wallets/create_wallet.html", {"form": form})
            wallet = form.save(commit=False)
            wallet.owner = request.user
            wallet.save()
            messages.success(request, "Wallet created successfully!")
            return redirect('wallets:wallets')
    else:
        form = AccountForm()
    return render(request, "wallets/create_wallet.html", {"form": form})

@login_required
def delete_wallet(request, pk):
    wallet = get_object_or_404(Account.objects.select_related('owner'), pk=pk, owner=request.user)
    if wallet.balance > 0:
        other_wallets = request.user.accounts.exclude(pk=wallet.pk).only('id', 'name', 'currency')
        if not other_wallets.exists():
            messages.error(request, "You cannot delete this wallet with a positive balance because you have no other wallets to transfer the funds to.")
            return redirect('wallets:wallets')
        if request.method == "POST":
            target_pk = request.POST.get("target_wallet")
            target_wallet = get_object_or_404(Account, pk=target_pk, owner=request.user)
            Transaction.objects.create(
                account_from=wallet,
                account_to=target_wallet,
                txn_type='p2p',
                amount=wallet.balance,
                currency=wallet.currency,
                status='completed'
            )
            wallet.delete()
            messages.success(request, "Wallet deleted, funds transferred.")
            return redirect('wallets:wallets')
        return render(request, "wallets/confirm_delete_wallet.html", {
            "wallet": wallet,
            "other_wallets": other_wallets,
        })
    else:
        if request.method == "POST":
            wallet.delete()
            messages.success(request, "Wallet deleted.")
            return redirect('wallets:wallets')
        return render(request, "wallets/confirm_delete_wallet.html", {"wallet": wallet})

@login_required
def topup_wallet(request, pk):
    wallet = get_object_or_404(Account.objects.select_related('owner'), pk=pk, owner=request.user)
    if request.method == "POST":
        form = TopUpForm(request.POST)
        if form.is_valid():
            Transaction.objects.create(
                account_to=wallet,
                txn_type='topup',
                amount=form.cleaned_data['amount'],
                currency=wallet.currency,
                status='completed'
            )
            messages.success(request, f"Wallet topped up by {form.cleaned_data['amount']} {wallet.currency.upper()}!")
            return redirect('wallets:wallets')
    else:
        form = TopUpForm()
    return render(request, "wallets/topup_wallet.html", {"form": form, "wallet": wallet})

@login_required
def transfer_wallet(request):
    accounts = request.user.accounts.all()
    if accounts.count() < 2:
        messages.error(request, "You need at least two wallets to make a transfer.")
        return redirect('wallets:wallets')

    if request.method == "POST":
        form = TransferForm(request.user, request.POST)
        if form.is_valid():
            from_wallet = form.cleaned_data['from_wallet']
            to_wallet = form.cleaned_data['to_wallet']
            amount = form.cleaned_data['amount']
            rate = Decimal("1")
            if from_wallet.currency != to_wallet.currency:
                rate = Decimal(str(getattr(settings, "CURRENCY_RATES", {}).get(
                    (from_wallet.currency.upper(), to_wallet.currency.upper()), 1
                )))
            converted_amount = round(amount * rate, 2)

            if amount > from_wallet.balance:
                messages.error(request, "Not enough funds.")
            else:

                Transaction.objects.create(
                    account_from=from_wallet,
                    account_to=to_wallet,
                    txn_type='p2p',
                    amount=amount,
                    currency=from_wallet.currency,
                    status='completed'
                )
                Transaction.objects.create(
                    account_from=from_wallet,
                    account_to=to_wallet,
                    txn_type='p2p',
                    amount=converted_amount,
                    currency=to_wallet.currency,
                    status='completed'
                )
                messages.success(
                    request,
                    f"Transferred {amount} {from_wallet.currency.upper()} → {converted_amount} {to_wallet.currency.upper()}"
                )
                return redirect('wallets:wallets')
    else:
        form = TransferForm(request.user)
    return render(request, "wallets/transfer_wallet.html", {"form": form})