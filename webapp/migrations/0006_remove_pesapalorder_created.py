# Generated by Django 3.2.5 on 2021-07-25 18:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_auto_20210725_1821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pesapalorder',
            name='created',
        ),
    ]
