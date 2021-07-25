import datetime
import urllib.parse  # To URLencode the parameter string
import time
import json
import pesapal

import requests
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

from requests_oauthlib import OAuth1, OAuth1Session

from webapp.forms import UserForm
from webapp import models


# Create your views here.
def home_view(request):
    # Instantiate a dictionary for context to be rendered with html
    context = dict()
    if request.method == 'GET':
        context = {'donor_form': UserForm()}
    elif request.method == 'POST':
        donor_form = UserForm(data=request.POST)
        if donor_form.is_valid():
            first_name = donor_form.cleaned_data['first_name']
            last_name = donor_form.cleaned_data['last_name']
            email = donor_form.cleaned_data['email']
            amount = donor_form.cleaned_data['amount']
            next_billing_date_monthly = donor_form.cleaned_data['next_billing_date_monthly']
            next_billing_date_annual = donor_form.cleaned_data['next_billing_date_annual']
            bill_period = donor_form.cleaned_data['bill_period']
            if not User.objects.filter(email=email).exists():
                print('1')
                user = User.objects.create(username=generate_username(), first_name=first_name.upper(),
                                           last_name=last_name.upper(), email=email)
                donor = models.UserContributionConf.objects.create(amount=amount, user=user, bill_period=bill_period)
                if next_billing_date_monthly is not None:
                    donor.next_billing_date = next_billing_date_monthly
                if next_billing_date_annual is not None:
                    donor.next_billing_date = next_billing_date_annual
                donor.save()
                models.PesaPalOrder.objects.create(user=user, amount=amount, reference=user.email)

            elif User.objects.filter(email=email, first_name=first_name.upper(),
                                     last_name=last_name.upper()).count() == 1:
                print('2')
                donor = models.UserContributionConf.objects.get(user=User.objects.get(email=email))
                donor.amount = amount
                donor.bill_period = bill_period
                if next_billing_date_monthly is not None:
                    donor.next_billing_date = next_billing_date_monthly
                if next_billing_date_monthly is not None:
                    donor.next_billing_date = next_billing_date_monthly
                donor.save()
                models.PesaPalOrder.objects.create(user=donor.user, amount=amount, reference=donor.user.email)
            else:
                return HttpResponse('Your details should match!')

            pesapal.consumer_key = models.PesaPalCredentials.objects.first().pesapal_consumer_key
            pesapal.consumer_secret = models.PesaPalCredentials.objects.first().pesapal_consumer_secret
            pesapal.testing = False
            order_reference_id = list(models.PesaPalOrder.objects.filter(user=User.objects.get(email=email)))[-1]
            post_params = {
                'oauth_callback': f'http:localhost:8000/order/success/{order_reference_id} '
            }
            request_data = {
                'FirstName': f'{first_name}',
                'LastName': f'{last_name}',
                'Amount': f'{amount}',
                'Description': f'A Donation of KES {amount}',
                'Type': 'MERCHANT',
                'Reference': f'{order_reference_id}',
                'Email': f'{email}'
            }
            # build url to redirect user to confirm payment
            url = pesapal.postDirectOrder(post_params, request_data)
            pesapal_query_payment_url = 'https://www.pesapal.com/API/QueryPaymentStatus'
            return HttpResponseRedirect(redirect_to=url)
        else:
            print('invalid')
            print(donor_form.errors)
            context = {'donor_form': UserForm(data=donor_form.data)}
    return render(request, 'webapp/home.html', context, 'text/html', 200)


def donation_complete(request):
    return HttpResponse("Thank You")


def generate_username():
    username = 'user-' + str(User.objects.latest('date_joined').id+1)
    if User.objects.filter(username=username).exists():
        return generate_username()
    return username
