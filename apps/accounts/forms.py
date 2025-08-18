from django import forms
from .models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'type', 'currency']


class TopUpForm(forms.Form):
    amount = forms.DecimalField(label="Amount", min_value=0.01, max_digits=10, decimal_places=2)

class TransferForm(forms.Form):
    from_wallet = forms.ModelChoiceField(queryset=None, label="From wallet")
    to_wallet = forms.ModelChoiceField(queryset=None, label="To wallet")
    amount = forms.DecimalField(label="Amount", min_value=0.01, max_digits=10, decimal_places=2)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        wallets = user.accounts.all()
        self.fields['from_wallet'].queryset = wallets
        self.fields['to_wallet'].queryset = wallets

        # Показывать баланс в выпадающем списке
        self.fields['from_wallet'].label_from_instance = self.wallet_label
        self.fields['to_wallet'].label_from_instance = self.wallet_label

        if 'from_wallet' in self.data:
            try:
                from_wallet_id = int(self.data.get('from_wallet'))
                self.fields['to_wallet'].queryset = wallets.exclude(pk=from_wallet_id)
            except (ValueError, TypeError):
                pass

    def wallet_label(self, wallet):
        return f"{wallet.name} ({wallet.currency.upper()}) — {wallet.balance:.2f} {wallet.currency.upper()}"