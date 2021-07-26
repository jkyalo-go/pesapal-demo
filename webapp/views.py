import datetime
import threading
import urllib.parse  # To URLencode the parameter string
import time
import json
import pesapal
import pytz
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
        url = ''
        if donor_form.is_valid():
            first_name = donor_form.cleaned_data['first_name']
            last_name = donor_form.cleaned_data['last_name']
            email = donor_form.cleaned_data['email']
            amount = donor_form.cleaned_data['amount']
            next_billing_date_monthly = donor_form.cleaned_data['next_billing_date_monthly']
            next_billing_date_annual = donor_form.cleaned_data['next_billing_date_annual']
            bill_period = donor_form.cleaned_data['bill_period']
            if not User.objects.filter(email=email).exists():
                user = User.objects.create(username=generate_username(), first_name=first_name.upper(),
                                           last_name=last_name.upper(), email=email)
                donor = models.UserContributionConf.objects.create(amount=amount, user=user, bill_period=bill_period)
                set_billing_period(bill_period, donor, next_billing_date_annual, next_billing_date_monthly)
                models.PesaPalOrder.objects.create(user=user, amount=amount, reference=user.email)
            elif User.objects.filter(email=email, first_name=first_name.upper(),
                                     last_name=last_name.upper()).count() == 1:
                models.UserContributionConf.objects.get_or_create(user=User.objects.get(
                    email=email), amount=amount)
                donor = models.UserContributionConf.objects.get(user=User.objects.get(email=email))
                donor.bill_period = bill_period
                set_billing_period(bill_period, donor, next_billing_date_annual, next_billing_date_monthly)
                models.PesaPalOrder.objects.create(user=donor.user, amount=amount, reference=donor.user.email)
            else:
                return HttpResponse('Your details should match!')
            donor = models.UserContributionConf.objects.get(user=User.objects.get(email=email))

            if bill_period == 'once':
                url = make_payment(amount, email, first_name, last_name)
            elif bill_period == 'monthly':
                # check whether today is the day to donate if so initiate payment
                if datetime.date.today() == donor.next_billing_date:
                    url = make_payment(amount, email, first_name, last_name)
                    donor.next_billing_date = validate_next_billing_date(day=donor.day)
                else:
                    # TODO: redirect user to about page
                    pass
            elif bill_period == 'annual':
                # check whether today is the day to donate if so initiate payment
                if datetime.date.today() == donor.next_billing_date:
                    url = make_payment(amount, email, first_name, last_name)
                    donor.next_billing_date = validate_next_billing_date(day=donor.day, month=donor.month)
                else:
                    # TODO: redirect user to about page
                    pass
            donor.save()
            return HttpResponseRedirect(redirect_to=url)
        else:
            print('invalid')
            print(donor_form.errors)
            context = {'donor_form': UserForm(data=donor_form.data)}
    return render(request, 'webapp/home.html', context, 'text/html', 200)


def make_payment(amount, email, first_name, last_name):
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
    return url


def set_billing_period(bill_period, donor, next_billing_date_annual, next_billing_date_monthly):
    if bill_period == 'once':
        donor.next_billing_date = None
    if bill_period == 'monthly':
        donor.day = next_billing_date_monthly.day
        donor.month = None
        # validate next billing date
        donor.next_billing_date = validate_next_billing_date(day=next_billing_date_monthly.day)
    if bill_period == 'annual':
        donor.day = next_billing_date_annual.day
        donor.month = next_billing_date_annual.month
        donor.next_billing_date = validate_next_billing_date(day=next_billing_date_annual.day,
                                                             month=next_billing_date_annual.month)
    donor.save()


def donation_complete(request):
    pesapal_transaction_tracking_id = request.GET.get('pesapal_transaction_tracking_id', None)
    pesapal_merchant_reference = request.GET.get('pesapal_merchant_reference', None)
    order = models.PesaPalOrder.objects.get(reference=pesapal_merchant_reference)
    order.tracking_id = pesapal_transaction_tracking_id
    order.save()
    donor = models.UserContributionConf.objects.get(user==order.user)
    if donor.bill_period == 'monthly':
        donor.next_billing_date = validate_next_billing_date(day=donor.day, month_forward=True)
    elif donor.bill_period == 'annual':
        donor.next_billing_date = validate_next_billing_date(month=donor.month, year_forward=True)
    return HttpResponse("Thank You! for your donation.")


def generate_username():
    username = 'user-' + str(User.objects.latest('date_joined').id + 1)
    if User.objects.filter(username=username).exists():
        return generate_username()
    return username


def validate_next_billing_date(day=None, month=None, month_forward=False, year_forward=False):
    today = datetime.date.today()
    next_bill_date = None
    if day is not None and month is None:
        if not month_forward:
            try:
                next_bill_date = today.replace(day=day)
            except ValueError:
                return validate_next_billing_date(day=day - 1)
            if next_bill_date < today:
                return validate_next_billing_date(day=day, month_forward=True)
        else:
            try:
                next_bill_date = (today + datetime.timedelta(days=20)).replace(day=day)
            except ValueError:
                return validate_next_billing_date(day=day - 1, month=month)
    if day is not None and month is not None:
        if not year_forward:
            try:
                next_bill_date = today.replace(day=day, month=month)
            except ValueError:
                return validate_next_billing_date(day=day - 1, month=month)
            if next_bill_date < today:
                return validate_next_billing_date(day=day, month=month, year_forward=True)
        else:
            try:
                next_bill_date = today.replace(day=day, month=month, year=today.year + 1)
            except ValueError:
                return validate_next_billing_date(day=day - 1, month=month, year_forward=True)

    return next_bill_date


def send_billing_mail():
    users = models.UserContributionConf.objects.all()
    us = models.EmailService.objects.first().email_address
    for user in users:
        if datetime.date.today() == user.next_billing_date:
            you = user.user.email
            message = MIMEMultipart('alternative')
            message['Subject'] = f'{user.bill_period.capitalize()} Donation'
            message['From'] = us
            message['To'] = you
            redirect_url = make_payment(user.amount, user.user.email, user.user.first_name, user.user.last_name)
            text = f'Dear {user.user.first_name}, Your {user.bill_period.capitalize()} Donation is due Today({datetime.date.today()}). <p>Direct link to payment: {redirect_url}</p> '
            html = f'<html><head></head><body>Dear <b>{user.user.first_name}<\b>, Your {user.bill_period.capitalize()}' \
                   f' Donation is due Today({datetime.date.today()}). <p>Direct link to payment: {redirect_url}</p> ' \
                   f'</body></html> '

            text_content = MIMEText(text, 'plain')
            html_content = MIMEText(html, 'html')

            message.attach(text_content)
            message.attach(html_content)
            session = smtplib.SMTP(models.EmailService.objects.first().email_host,
                                   models.EmailService.objects.first().email_host_port)
            session.login(us, models.EmailService.objects.first().email_address_password)
            session.sendmail(us, you, message.as_string())
            session.quit()


def schedule_send_mail():
    thread = threading.Thread(target=send_billing_mail)
    thread.setDaemon(True)
    thread.start()

