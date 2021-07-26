# Generated by Django 3.2.5 on 2021-07-25 18:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20210725_1816'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pesapalorder',
            options={'get_latest_by': ['created']},
        ),
        migrations.AddField(
            model_name='pesapalorder',
            name='created',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]