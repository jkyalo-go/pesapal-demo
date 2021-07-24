from django.db import models
from django.contrib.auth.models import User

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
    next_billing_date = models.DateField()
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
