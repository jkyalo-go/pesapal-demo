from django.contrib import admin
from webapp import models

# Register your models here.
admin.site.register(models.PesaPalCredentials)
admin.site.register(models.UserContributionConf)
admin.site.register(models.PesaPalOrder)
admin.site.register(models.EmailService)
