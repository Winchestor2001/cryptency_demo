# Generated by Django 4.1 on 2022-08-31 16:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminConfigs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_bonus', models.IntegerField(verbose_name='Реф.бонус')),
                ('withdraw_sum', models.IntegerField(verbose_name='Мин. сумма вывода')),
                ('card_number', models.BigIntegerField(verbose_name='Номер карты')),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=100, verbose_name='Название сервиса')),
                ('service_title', models.CharField(max_length=100, verbose_name='Загаловка сервиса')),
                ('service_description', models.CharField(max_length=100, verbose_name='Описание сервиса')),
                ('service_price', models.CharField(max_length=100, verbose_name='Цена сервиса')),
            ],
        ),
        migrations.CreateModel(
            name='UserSecureData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100, null=True, verbose_name='Имя')),
                ('user_surname', models.CharField(max_length=150, null=True, verbose_name='Фаимилия')),
                ('user_middle_name', models.CharField(max_length=150, null=True, verbose_name='Отчество')),
                ('user_birthday', models.DateField(null=True, verbose_name='Дата рождения')),
                ('user_country', models.CharField(max_length=150, null=True, verbose_name='Страна')),
                ('user_city', models.CharField(max_length=100, null=True, verbose_name='Город')),
                ('user_index', models.CharField(max_length=30, null=True, verbose_name='Индекс')),
                ('user_street', models.CharField(max_length=150, null=True, verbose_name='Улица')),
                ('user_home', models.CharField(max_length=50, null=True, verbose_name='Дом')),
                ('user_corpus', models.CharField(max_length=150, null=True, verbose_name='Корпус')),
                ('user_room', models.CharField(max_length=150, null=True, verbose_name='Тип помещения')),
                ('user_room_num', models.CharField(max_length=10, null=True, verbose_name='№')),
                ('user_pass_seria', models.CharField(max_length=10, null=True, verbose_name='Серия')),
                ('user_pass_num', models.CharField(max_length=10, null=True, verbose_name='Номер паспорта')),
                ('user_pass_date_issue', models.CharField(max_length=10, null=True, verbose_name='Дата выдачи')),
                ('user_pass_issued_by', models.CharField(max_length=10, null=True, verbose_name='Кем выдан')),
                ('user_departmen_code', models.CharField(max_length=10, null=True, verbose_name='Код подразделения')),
                ('user_place_of_birth', models.CharField(max_length=10, null=True, verbose_name='Место рождения')),
                ('user_country_subject', models.CharField(max_length=150, null=True, verbose_name='Субъект Федерации')),
                ('user_country_of_operation', models.CharField(max_length=150, null=True, verbose_name='Страна деятельности')),
                ('user_country_of_operation_status', models.CharField(max_length=200, null=True, verbose_name='Статус в стране деятельности')),
                ('user_email', models.CharField(max_length=50, null=True, unique=True, verbose_name='E-mail')),
                ('user_pass_photo1', models.ImageField(blank=True, null=True, upload_to='users_doc/')),
                ('user_pass_photo2', models.ImageField(blank=True, null=True, upload_to='users_doc/')),
            ],
        ),
        migrations.CreateModel(
            name='UsersEmailVerifyTokens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.CharField(max_length=50, unique=True, verbose_name='E-mail')),
                ('user_token', models.CharField(max_length=255, verbose_name='Токен')),
            ],
        ),
        migrations.CreateModel(
            name='UsersPayChecks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_pay_check', models.ImageField(blank=True, null=True, upload_to='users_pay_check/', verbose_name='Чек об оплате')),
                ('user_email', models.CharField(max_length=50, verbose_name='E-mail')),
                ('service_name', models.CharField(max_length=100, verbose_name='Название сервиса')),
                ('service_pk', models.IntegerField(unique=True, verbose_name='ID сервиса')),
                ('user_pay_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')),
            ],
        ),
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_title', models.CharField(max_length=100, verbose_name='Загаловка видео')),
                ('video_link', models.CharField(max_length=100, verbose_name='Ссылка видео')),
                ('service_pk', models.IntegerField(verbose_name='ID сервиса')),
            ],
        ),
        migrations.CreateModel(
            name='UsersProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100, verbose_name='Имя')),
                ('user_surname', models.CharField(max_length=150, verbose_name='Фаимилия')),
                ('user_email', models.CharField(max_length=50, unique=True, verbose_name='E-mail')),
                ('user_password', models.CharField(max_length=50, verbose_name='Пароль')),
                ('user_photo', models.ImageField(null=True, upload_to='users_avatar/', verbose_name='Аватарка')),
                ('user_referals', models.IntegerField(default=0, verbose_name='Рефералы')),
                ('user_referals_link', models.CharField(default='none', max_length=200, null=True, verbose_name='Реферальная ссылка')),
                ('user_balance', models.BigIntegerField(default=0, verbose_name='Баланс')),
                ('user_referals_bonus', models.BigIntegerField(default=0, verbose_name='Реферальная награждение')),
                ('user_reg_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')),
                ('user_email_verify', models.BooleanField(default=False, verbose_name='Проверка e-mail')),
                ('user_verify', models.BooleanField(default=False, verbose_name='Верификация')),
                ('user_referal_email1', models.CharField(default='none', max_length=50, null=True, verbose_name='Реферал по E-mail уровень-1')),
                ('user_referal_email2', models.CharField(default='none', max_length=50, null=True, verbose_name='Реферал по E-mail уровень-2')),
                ('user_referal_email3', models.CharField(default='none', max_length=50, null=True, verbose_name='Реферал по E-mail уровень-3')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
