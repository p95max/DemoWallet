from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import TransferForm
from .models import Transfer
from apps.accounts.models import Account
from apps.transactions.models import Transaction
from decimal import Decimal

@login_required
def send_transfer(request):
    if request.method == "POST":
        form = TransferForm(request.user, request.POST)
        if form.is_valid():
            to_user = form.cleaned_data['to_user']
            from_account = form.cleaned_data['from_account']
            amount = form.cleaned_data['amount']
            message = form.cleaned_data['message']

            to_account = Account.objects.filter(owner=to_user, currency=from_account.currency).first()
            if not to_account:
                messages.error(request, "Recipient has no wallet in this currency.")
                return render(request, "transfers/send_transfer.html", {"form": form})

            if amount > from_account.balance:
                messages.error(request, "Not enough funds.")
                return render(request, "transfers/send_transfer.html", {"form": form})

            transfer = Transfer.objects.create(
                sender=request.user,
                receiver=to_user,
                from_account=from_account,
                to_account=to_account,
                amount=amount,
                currency=from_account.currency,
                message=message,
                status='completed'
            )
            Transaction.objects.create(
                account_from=from_account,
                account_to=to_account,
                txn_type='p2p',
                amount=amount,
                currency=from_account.currency,
                status='completed'
            )
            Transaction.objects.create(
                account_from=from_account,
                account_to=to_account,
                txn_type='p2p',
                amount=amount,
                currency=to_account.currency,
                status='completed'
            )
            messages.success(request, f"Transfer sent to {to_user.username}!")
            return redirect('wallets:wallets')
    else:
        form = TransferForm(request.user)
    return render(request, "transfers/send_transfer.html", {"form": form})