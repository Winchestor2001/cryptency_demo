from django.db import models
from django.contrib.auth.models import User


class UsersProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100, verbose_name='Имя')
    user_surname = models.CharField(max_length=150, verbose_name='Фаимилия')
    user_country = models.CharField(max_length=150, verbose_name='Страна')
    user_email = models.CharField(max_length=50, unique=True, verbose_name='E-mail')
    user_password = models.CharField(max_length=50, verbose_name='Пароль')
    user_photo = models.ImageField(upload_to='users_avatar/', blank=True, null=True, verbose_name='Аватарка')
    user_referals = models.IntegerField(default=0, verbose_name='Рефералы')
    user_referals_link = models.CharField(max_length=200, null=True, default='none', verbose_name='Реферальная ссылка')
    user_balance = models.BigIntegerField(default=0, verbose_name='Баланс')
    user_referals_bonus = models.BigIntegerField(default=0, verbose_name='Реферальная награждение')
    user_reg_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    user_email_verify = models.BooleanField(default=False, verbose_name='Проверка e-mail')
    user_verify = models.BooleanField(default=False, verbose_name='Верификация')
    user_referal_email1 = models.CharField(max_length=50, default='none', null=True,
                                           verbose_name='Реферал по E-mail уровень-1')
    user_referal_email2 = models.CharField(max_length=50, default='none', null=True,
                                           verbose_name='Реферал по E-mail уровень-2')
    user_referal_email3 = models.CharField(max_length=50, default='none', null=True,
                                           verbose_name='Реферал по E-mail уровень-3')

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = "Профиль клиента"
        verbose_name_plural = "Профиль клиентов"


class UsersEmailVerifyTokens(models.Model):
    user_email = models.CharField(max_length=50, unique=True, verbose_name='E-mail')
    user_token = models.CharField(max_length=255, verbose_name='Токен')

    def __str__(self):
        return self.user_email

    class Meta:
        verbose_name = "Верификация почты"
        verbose_name_plural = "Верификация почты"


class UserSecureData(models.Model):
    user_name = models.CharField(max_length=100, verbose_name='Имя', null=True)
    user_surname = models.CharField(max_length=150, verbose_name='Фаимилия', null=True)
    user_birthday = models.DateField(verbose_name='Дата рождения', null=True)
    user_pass_seria = models.CharField(max_length=10, verbose_name='Серия', null=True)
    user_pass_num = models.CharField(max_length=10, verbose_name='Номер паспорта', null=True)
    user_pass_date_issue = models.CharField(max_length=10, verbose_name='Дата выдачи', null=True)
    user_pass_issued_by = models.CharField(max_length=10, verbose_name='Кем выдан', null=True)
    user_departmen_code = models.CharField(max_length=10, verbose_name='Код подразделения', null=True)
    user_place_of_birth = models.CharField(max_length=10, verbose_name='Место рождения', null=True)
    user_email = models.CharField(max_length=50, unique=True, verbose_name='E-mail', null=True)
    user_pass_photo1 = models.ImageField(upload_to='users_doc/', null=True, blank=True)
    user_pass_photo2 = models.ImageField(upload_to='users_doc/', null=True, blank=True)

    def __str__(self):
        return self.user_email

    class Meta:
        verbose_name = "Данные о клиенте"
        verbose_name_plural = "Данные о клиентах"


class Services(models.Model):
    CHOICES = (
        ('BYN', 'byn'),
        ('USD', 'usd')
    )
    service_name = models.CharField(max_length=100, verbose_name='Название сервиса')
    service_title = models.CharField(max_length=100, verbose_name='Загаловка сервиса')
    service_description = models.TextField(verbose_name='Описание сервиса')
    service_price1 = models.CharField(max_length=100, verbose_name='Цена сервиса на USD')
    service_price2 = models.CharField(max_length=100, verbose_name='Цена сервиса на BYN')
    # service_simbole = models.CharField(max_length=20, choices=CHOICES, verbose_name='Символ')

    def __str__(self):
        return self.service_name

    class Meta:
        verbose_name = "Сервис"
        verbose_name_plural = "Сервисы"


class AdminConfigs(models.Model):
    ref_bonus1 = models.IntegerField(verbose_name='Реф.бонус 1 уровень')
    ref_bonus2 = models.IntegerField(verbose_name='Реф.бонус 2 уровень')
    ref_bonus3 = models.IntegerField(verbose_name='Реф.бонус 3 уровень')
    withdraw_sum = models.IntegerField(verbose_name='Мин. сумма вывода')
    card_number = models.CharField(max_length=100, verbose_name='Номер карты')

    class Meta:
        verbose_name = "Админ конфигурация"
        verbose_name_plural = "Админ конфигурации"


class UsersPayChecks(models.Model):
    user_pay_check = models.ImageField(upload_to='users_pay_check/', blank=True, null=True, verbose_name='Чек об оплате')
    user_email = models.CharField(max_length=50, verbose_name='E-mail')
    service_name = models.CharField(max_length=100, verbose_name='Название сервиса')
    service_pk = models.IntegerField(unique=True, verbose_name='ID сервиса')
    user_pay_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    paid = models.BooleanField(default=False, verbose_name="Оплатил?")

    def __str__(self):
        return self.user_email

    class Meta:
        verbose_name = "Проверка оплат"
        verbose_name_plural = "Проверка оплаты"


class Videos(models.Model):
    video_title = models.CharField(max_length=100, verbose_name='Загаловка видео')
    video_link = models.CharField(max_length=100, verbose_name='Ссылка видео')
    video_data = models.FileField(upload_to='service_videos/', blank=True, null=True, verbose_name='Видео')
    service_pk = models.IntegerField(verbose_name='ID сервиса')

    def __str__(self):
        return self.video_title

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
