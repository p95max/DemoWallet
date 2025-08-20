from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from apps.transactions.models import Transaction


def main_page(request):
    return render(request, 'index.html')

@login_required
def dashboard_page(request):
    accounts = request.user.accounts.all()
    total_balance = sum(acc.balance for acc in accounts)
    balances_by_currency = {}
    for acc in accounts:
        balances_by_currency.setdefault(acc.currency, 0)
        balances_by_currency[acc.currency] += acc.balance

    notifications = request.user.notifications.order_by('-created_at')[:5]

    user_wallets = accounts.values_list('pk', flat=True)
    transactions = (
        Transaction.objects
        .filter(Q(account_from__in=user_wallets) | Q(account_to__in=user_wallets))
        .select_related('account_from', 'account_to')
        .order_by('-created_at')[:5]
    )

    return render(request, "dashboard.html", {
        "accounts": accounts,
        "total_balance": total_balance,
        "balances_by_currency": balances_by_currency,
        "notifications": notifications,
        "transactions": transactions,
    })
