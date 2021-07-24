from django import forms
from django.contrib.auth.models import User

from webapp.models import UserContributionConf, BILLING_PERIOD


class UserForm(forms.ModelForm):
    amount = forms.FloatField()
    bill_period = forms.ChoiceField(choices=BILLING_PERIOD, widget=forms.Select(attrs={
        'onchange': 'showInputField(this.value)'}))
    next_billing_date_monthly = forms.DateField(required=False, label='Billed monthly on',
                                                widget=forms.SelectDateWidget(years=['2021'], attrs={
                                                    'form': 'donor-form'}))
    next_billing_date_annual = forms.DateField(required=False, label='Billed annual on', widget=forms.SelectDateWidget(
        years=['2021'], attrs={'form': 'donor-form'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'amount', 'bill_period', 'next_billing_date_monthly',
                  'next_billing_date_annual']
