# Generated by Django 3.2.5 on 2021-07-26 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0010_auto_20210726_0251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailservice',
            name='email_host',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='emailservice',
            name='email_host_port',
            field=models.IntegerField(),
        ),
    ]
