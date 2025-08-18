from django import forms
from django.contrib.auth import get_user_model
from apps.accounts.models import Account

class TransferForm(forms.Form):
    to_user = forms.ModelChoiceField(queryset=None, label="Send to user")
    from_account = forms.ModelChoiceField(queryset=None, label="From your wallet")
    to_account = forms.ModelChoiceField(queryset=None, label="To wallet")
    amount = forms.DecimalField(label="Amount", min_value=0.01, max_digits=10, decimal_places=2)
    message = forms.CharField(label="Message", max_length=255, required=False)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        User = get_user_model()
        self.fields['to_user'].queryset = User.objects.exclude(pk=user.pk)
        self.fields['from_account'].queryset = user.accounts.all()
        self.fields['from_account'].label_from_instance = self.account_label_with_balance

        self.fields['to_account'].label_from_instance = self.account_label_simple

        if 'to_user' in self.data:
            try:
                to_user_id = int(self.data.get('to_user'))
                self.fields['to_account'].queryset = Account.objects.filter(owner_id=to_user_id)
            except (ValueError, TypeError):
                self.fields['to_account'].queryset = Account.objects.none()
        elif self.initial.get('to_user'):
            to_user_id = self.initial['to_user'].id
            self.fields['to_account'].queryset = Account.objects.filter(owner_id=to_user_id)
        else:
            self.fields['to_account'].queryset = Account.objects.none()

    def account_label_with_balance(self, account):
        return f"{account.name} ({account.currency.upper()}) — {account.balance:.2f} {account.currency.upper()}"

    def account_label_simple(self, account):
        return f"{account.name} ({account.currency.upper()})"