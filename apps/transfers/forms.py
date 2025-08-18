from django import forms
from django.contrib.auth import get_user_model
from apps.accounts.models import Account

class TransferForm(forms.Form):
    to_user = forms.ModelChoiceField(queryset=None, label="Send to user")
    from_account = forms.ModelChoiceField(queryset=None, label="From your wallet")
    amount = forms.DecimalField(label="Amount", min_value=0.01, max_digits=10, decimal_places=2)
    message = forms.CharField(label="Message", max_length=255, required=False)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        User = get_user_model()
        self.fields['to_user'].queryset = User.objects.exclude(pk=user.pk)
        self.fields['from_account'].queryset = user.accounts.all()