# Generated by Django 4.1 on 2022-08-31 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptency', '0005_remove_usersecuredata_user_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminconfigs',
            name='card_number',
            field=models.CharField(max_length=100, verbose_name='Номер карты'),
        ),
    ]