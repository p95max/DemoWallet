from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

@login_required
def all_transactions(request):
    user_wallets = request.user.accounts.values_list('pk', flat=True)
    transactions = (
        Transaction.objects
        .filter(Q(account_from__in=user_wallets) | Q(account_to__in=user_wallets))
        .select_related('account_from', 'account_to')
        .order_by('-created_at')
    )
    return render(request, "transactions/all_transactions.html", {
        "transactions": transactions,
    })

@login_required
def transaction_detail(request, pk):
    user_wallets = request.user.accounts.values_list('pk', flat=True)
    transaction = get_object_or_404(
        Transaction.objects.filter(
            Q(pk=pk) & (Q(account_from__in=user_wallets) | Q(account_to__in=user_wallets))
        )
    )
    context = {
        "transaction": transaction,
    }

    return render(request, "transactions/transaction_detail.html", context=context)