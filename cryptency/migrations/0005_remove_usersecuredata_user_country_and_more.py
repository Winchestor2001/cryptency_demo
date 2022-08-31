# Generated by Django 4.1 on 2022-08-31 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptency', '0004_remove_usersecuredata_user_city_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersecuredata',
            name='user_country',
        ),
        migrations.AddField(
            model_name='usersprofile',
            name='user_country',
            field=models.CharField(default='russia', max_length=150, verbose_name='Страна'),
            preserve_default=False,
        ),
    ]
