# Generated by Django 4.1 on 2022-08-31 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptency', '0007_userspaychecks_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='service_simbole',
            field=models.CharField(choices=[('BYN', 'byn'), ('USD', 'usd')], default='usd', max_length=20, verbose_name='Символ'),
            preserve_default=False,
        ),
    ]