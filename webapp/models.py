import datetime

from django.db import models
from django.contrib.auth.models import User
import hashlib

# List of billing period choices
BILLING_PERIOD = [
    ('once', 'Billed Once'),
    ('monthly', 'Billed Monthly'),
    ('annual', 'Billed Annual'),
]


# Create your models here.
# Extended default django User Model to form user contribution profile
class UserContributionConf(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    next_billing_date = models.DateField(blank=True, null=True)
    bill_period = models.CharField(max_length=255, default=BILLING_PERIOD[0][0], choices=BILLING_PERIOD)


# Model used to keep record of donations
class Donation(models.Model):
    donation_by = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    billed_on = models.DateField()


# Email Conf used to send monthly/annual notifications to donors based on time schedule of their donations
class EmailService(models.Model):
    email_host = models.URLField()
    email_host_port = models.IntegerField(default=587)
    email_address = models.EmailField()
    email_address_password = models.CharField(max_length=512)

    # Ensure only a single instance of email credentials is kept
    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)


class PesaPalCredentials(models.Model):
    pesapal_consumer_key = models.CharField(max_length=256)
    pesapal_consumer_secret = models.CharField(max_length=256)
    debug = models.BooleanField(default=True)

    # Ensure only a single instance of pesapal integration credentials is kept
    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)

    def __str__(self):
        return 'PesaPal Credentials'

    class Meta:
        verbose_name_plural = 'PesaPal Integration Credentials'


class PesaPalOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reference = models.CharField(max_length=256)
    tracking_id = models.CharField(max_length=256)
    amount = models.FloatField()

    def __str__(self):
        return str(self.user.email)

    class Meta:
        verbose_name_plural = 'Pesapal Donation Orders'

    @classmethod
    def generate_reference_id(cls, email):
        return hashlib.md5(
            (email + str(datetime.datetime.now().timestamp())).encode(encoding='utf-8')).hexdigest()
