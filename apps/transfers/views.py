from decimal import Decimal
from locale import currency

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from config import settings
from .forms import TransferForm
from apps.accounts.models import Account
from apps.transactions.models import Transaction
from rest_framework import viewsets, permissions
from .models import Transfer
from .serializers import TransferSerializer
from ..notifications.models import Notification


class TransferViewSet(viewsets.ModelViewSet):
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transfer.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user, status='completed')

@login_required
def send_transfer(request, from_user=None):
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

            if from_account.currency == to_account.currency:
                Transaction.objects.create(
                    account_from=from_account,
                    account_to=to_account,
                    txn_type='p2p',
                    amount=amount,
                    currency=from_account.currency,
                    status='completed',
                    message=message,
                )
            else:

                rate = Decimal(str(getattr(settings, "CURRENCY_RATES", {}).get(
                    (from_account.currency.upper(), to_account.currency.upper()), 1
                )))
                converted_amount = round(amount * rate, 2)
                Transaction.objects.create(
                    account_from=from_account,
                    account_to=to_account,
                    txn_type='p2p',
                    amount=amount,
                    currency=from_account.currency,
                    status='completed',
                    message=message,
                )
                Transaction.objects.create(
                    account_from=None,
                    account_to=to_account,
                    txn_type='p2p',
                    amount=converted_amount,
                    currency=to_account.currency,
                    status='completed',
                    message=message,
                )
            Notification.objects.create(
                recipient=to_user,
                notification_type='transfer',
                title='Funds received',
                message=f'You have received a transfer of {amount} {from_account.currency} from {request.user.email}'
            )
            messages.success(request, f"Transfer sent to {to_user.username}!")
            return redirect('wallets:wallets')
    else:
        form = TransferForm(request.user)
    return render(request, "transfers/send_transfer.html", {"form": form})