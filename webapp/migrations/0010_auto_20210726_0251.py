# Generated by Django 3.2.5 on 2021-07-26 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0009_auto_20210726_0246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercontributionconf',
            name='day',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='usercontributionconf',
            name='month',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]