import json
import random
import re
import secrets
import sys

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from django_cryptency import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from .models import UsersProfile, UsersEmailVerifyTokens, Services, UserSecureData, UsersPayChecks, Videos, \
    AdminConfigs, UsersWithdraw, UserReferalsService

# site_domen_link = 'http://127.0.0.1:8000'


site_domen_link = 'https://cryptency.by'
# site_domen_link = 'http://crypten1.iron.hostflyby.net'


def save_avatar(request, user_email):
    if request.FILES:
        file_obj = request.FILES['avatar']
        exten = file_obj.name.split('.')
        # filename = f'users_avatar/{user_email}.{exten[-1]}'
        filename = f'users_avatar/{user_email}.jpg'
        with default_storage.open(filename, 'wb+') as d:
            for chunk in file_obj.chunks():
                d.write(chunk)
        user = UsersProfile.objects.get(user_email=user_email)
        user.user_photo = filename
        user.save()


@login_required(login_url='user_login')
def home_page(request):
    if not request.user.is_staff:
        return redirect('profile')
    logout(request)
    return HttpResponseRedirect('/')


def user_reg(request, ref_link=None):
    configs = AdminConfigs.objects.all().values()
    context = {'conf_text': configs[0]['confidention_text'], 'conf_text2': configs[0]['user_data_confidention_text']}
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        pwd = request.POST['password1']
        country = request.POST['country']
        is_ref = request.POST['is_ref']
        usr_email = User.objects.filter(email=email)
        if usr_email:
            context['status'] = 'Такой email уже существует'
            return render(request, 'cryptency/signup.html', context=context)
        usr = User.objects.create_user(username=email, email=email, password=pwd)
        usr.first_name = name
        usr.last_name = surname
        usr.sert_id = "%05i" % (usr.id,)
        usr.save()
        token = secrets.token_hex(12)
        if is_ref:
            ref_user = UsersProfile.objects.get(user_email=is_ref)
            ref_user.user_referals += 1
            ref_user.save()
            reg = UsersProfile(user=usr, user_name=name, user_surname=surname, user_email=email, user_password=pwd,
                               user_country=country, user_referal_email1=is_ref,
                               user_referals_link=f'{site_domen_link}/user_referal/{token}')
            UsersEmailVerifyTokens(user_email=email, user_token=token).save()
        else:
            reg = UsersProfile(user=usr, user_name=name, user_surname=surname, user_email=email, user_password=pwd,
                               user_country=country, user_referals_link=f'{site_domen_link}/user_referal/{token}')
            UsersEmailVerifyTokens(user_email=email, user_token=token).save()
        reg.sert_id = "%05i" % (usr.id,)
        reg.save()
        context['status'] = 'Для продолжения работы подтвердите свою почту'
        html = render_to_string(
            'cryptency/email_body.html',
            {'verify_url': f'{site_domen_link}/auth/email_verify/{token}', 'domain': site_domen_link}
        )
        send_mail('Cryptency - подтверждение почты', 'Пожалуста подтвердите почту', settings.EMAIL_HOST_USER, [email],
                  html_message=html,
                  fail_silently=True)
        return render(request, 'cryptency/sended_email_code.html', context=context)

    if not ref_link is None:
        ref_user = UsersProfile.objects.get(user_referals_link=f"{site_domen_link}/user_referal/{ref_link}")
        context['is_ref'] = ref_user.user_email

    return render(request, 'cryptency/signup.html', context=context)


def user_login(request):
    context = {}
    if request.method == 'POST':
        email = request.POST['email']
        pwd = request.POST['password']
        try:
            usr = UsersProfile.objects.get(user_email=email)
            if usr.user_email_verify:
                user = authenticate(username=email, email=email, password=pwd)
                if user:
                    login(request, user)
                    return redirect('profile')
                else:
                    context['status'] = 'Почта или пароль не правильный'
            else:
                context['status'] = 'Ваша почта не подтверждена'
        except Exception as ex:
            print(ex)
            context['status'] = 'Эта почта не зарегистрирована'
    return render(request, 'cryptency/signin.html', context=context)


def reset_password(request):
    context = {}
    if request.method == 'POST':
        email = request.POST["email"]
        try:
            otp = secrets.token_hex(8)
            msz = f"Your new password is {otp}"
            try:
                user = User.objects.get(username=email)
                user2 = UsersProfile.objects.get(user_email=email)
                if not user2.user_email_verify:
                    context['email_status'] = 'Ваша почта не подтверждена'
                    context['email_color'] = 'danger'
                    return render(request, "cryptency/forgot_pass.html", context=context)
                send_mail("Check Account", msz, settings.EMAIL_HOST_USER, [user.email], fail_silently=True)
                user.set_password(otp)
                user2.user_password = otp
                user.save()
                user2.save()
                context['email_status'] = 'Новый пароль отправлен на почту!'
                context['email_color'] = 'success'
                return render(request, "cryptency/forgot_pass.html", context=context)
            except Exception as ex:
                print(ex)
                return redirect('home')
        except:
            context['status'] = 'Это почта не зарегистрирована'

    return render(request, "cryptency/forgot_pass.html", context=context)


@login_required
def user_logout(request):
    logout(request)
    res = HttpResponseRedirect('/')
    res.delete_cookie('user_id')
    res.delete_cookie('date_login')
    return res


@login_required
def user_profile(request):
    user = UsersProfile.objects.get(user_email=request.user.email)
    check_pay = UsersPayChecks.objects.filter(user_email=request.user.email).values()
    withdraws = UsersWithdraw.objects.filter(user_email=request.user.email).values()
    configs = AdminConfigs.objects.all().values()
    users_data = UserSecureData.objects.filter(user_email=request.user.email).values()
    purchase_status = 0
    user_buy_services = []
    if len(check_pay) != 0:
        for cp in check_pay:
            if cp['paid']:
                user_buy_services.append([cp['user_email'], cp['service_pk'], cp['service_name']])
                purchase_status += 1

    if len(users_data) != 0:
        verify1 = users_data[0]['user_verify']
        user.user_verify = verify1
        user.save()
    data = {
        'user_email': user.user_email,
        'user_referals_bonus': user.user_referals_bonus,
        'user_photo': user.user_photo,
        'user_name': user.user_name,
        'user_surname': user.user_surname,
        'user_balance': user.user_balance,
        'user_referals': user.user_referals,
        'user_verify': user.user_verify,
        'min_withdraw': configs[0]['withdraw_sum'],
        'user_verify2': False,
        'ref_link': user.user_referals_link if user.user_referals_link != 'none' else 'none',
        'user_reg_date': user.user_reg_date,
        'purchase_status': True if purchase_status != 0 else False,
    }
    if purchase_status != 0:
        for service in user_buy_services:
            services = Services.objects.get(pk=service[1])
            service_price = int(services.service_price1) / 100 * int(services.service_price_procent)
            check_ref_service = UserReferalsService.objects.filter(user_email=check_pay[0]['user_email']).filter(
                service_price_prosent=service_price).filter(service_name=f"{check_pay[0]['service_name']}")
            if len(check_ref_service) == 0:
                ref_email = user.user_referal_email1
                name = ''
                if not ref_email == 'none':
                    ref_user_data = UsersProfile.objects.get(user_email=ref_email)
                    ref_user_data.user_balance += service_price
                    ref_user_data.user_referals_bonus += service_price
                    name = ref_user_data.user_name
                    ref_user_data.save()
                UserReferalsService(user_email=check_pay[0]['user_email'], user_name=name,
                                    service_price_prosent=service_price,
                                    service_name=f"{check_pay[0]['service_name']}", ref_email=ref_email).save()
            else:
                select_refs = UserReferalsService.objects.filter(ref_email=request.user.email)
                if len(select_refs) != 0:
                    data['ref_static'] = select_refs
                else:
                    data['ref_static'] = False

    if user.user_verify and user.user_balance >= configs[0]['withdraw_sum']:
        data['user_verify'] = True,
        data['user_verify2'] = True,
    if len(withdraws) != 0:
        if not withdraws[0]['paid']:
            data['withdraw_cash'] = withdraws[0]['user_balance'],
        else:
            data['withdraw_cash'] = '0'
    if request.method == 'POST':
        save_avatar(request, request.user.email)
        return redirect('profile')
    return render(request, 'cryptency/user_profile.html', context=data)


@login_required
def user_profile_accrual(request):
    user = UsersProfile.objects.get(user_email=request.user)
    withdraws = UsersWithdraw.objects.filter(user_email=request.user.email).values()
    check_pay = UsersPayChecks.objects.filter(user_email=request.user.email).values()
    configs = AdminConfigs.objects.all().values()
    users_data = UserSecureData.objects.filter(user_email=request.user.email).values()
    purchase_status = 0
    user_buy_services = []
    if len(check_pay) != 0:
        for cp in check_pay:
            if cp['paid']:
                user_buy_services.append([cp['user_email'], cp['service_pk'], cp['service_name']])
                purchase_status += 1

    if len(users_data) != 0:
        verify1 = users_data[0]['user_verify']
        user.user_verify = verify1
        user.save()
    if purchase_status != 0:
        UserReferalsService(user_email=check_pay[0]['user_email'], service_price_prosent=check_pay[0]['user_email'],
                            service_name=f"{check_pay[0]['service_name']}").save()
    data = {
        'user_email': user.user_email,
        'user_referals_bonus': user.user_referals_bonus,
        'user_photo': user.user_photo,
        'user_name': user.user_name,
        'user_surname': user.user_surname,
        'user_balance': user.user_balance,
        'min_withdraw': configs[0]['withdraw_sum'],
        'user_referals': user.user_referals,
        'ref_link': user.user_referals_link if user.user_referals_link != 'none' else 'none',
        'user_verify': user.user_verify,
        'user_verify2': False,
        'user_reg_date': user.user_reg_date,
    }
    if purchase_status != 0:
        for service in user_buy_services:
            services = Services.objects.get(pk=service[1])
            service_price = int(services.service_price1) / 100 * int(services.service_price_procent)
            check_ref_service = UserReferalsService.objects.filter(user_email=check_pay[0]['user_email']).filter(
                service_price_prosent=service_price).filter(service_name=f"{check_pay[0]['service_name']}")
            if len(check_ref_service) == 0:
                ref_email = user.user_referal_email1
                name = ''
                if not ref_email == 'none':
                    ref_user_data = UsersProfile.objects.get(user_email=ref_email)
                    ref_user_data.user_balance += service_price
                    ref_user_data.user_referals_bonus += service_price
                    name = ref_user_data.user_name
                    ref_user_data.save()
                UserReferalsService(user_email=check_pay[0]['user_email'], user_name=name,
                                    service_price_prosent=service_price,
                                    service_name=f"{check_pay[0]['service_name']}", ref_email=ref_email).save()
            else:
                select_refs = UserReferalsService.objects.filter(ref_email=request.user.email)
                if len(select_refs) != 0:
                    data['ref_static'] = select_refs
                else:
                    data['ref_static'] = False
    if user.user_verify and user.user_balance >= configs[0]['withdraw_sum']:
        data['user_verify'] = True,
        data['user_verify2'] = True,
    if len(withdraws) != 0:
        if not withdraws[0]['paid']:
            data['withdraw_cash'] = withdraws[0]['user_balance'],
        else:
            data['withdraw_cash'] = '0'

    if request.method == 'POST':
        save_avatar(request, request.user.email)
    return render(request, 'cryptency/user_accrual.html', context=data)


@login_required
def user_profile_withdraws(request):
    user = UsersProfile.objects.get(user_email=request.user)
    withdraws = UsersWithdraw.objects.filter(user_email=request.user.email).values()
    check_pay = UsersPayChecks.objects.filter(user_email=request.user.email).values()
    configs = AdminConfigs.objects.all().values()
    users_data = UserSecureData.objects.filter(user_email=request.user.email).values()
    purchase_status = 0
    user_buy_services = []
    data = {
        'user_email': user.user_email,
        'purchase_status': True if purchase_status != 0 else False,
        'user_referals_bonus': user.user_referals_bonus,
        'user_photo': user.user_photo,
        'user_name': user.user_name,
        'user_surname': user.user_surname,
        'min_withdraw': configs[0]['withdraw_sum'],
        'user_balance': user.user_balance,
        'user_referals': user.user_referals,
        'ref_link': user.user_referals_link if user.user_referals_link != 'none' else 'none',
        'user_verify': user.user_verify,
        'user_verify2': False,
        'user_reg_date': user.user_reg_date,
    }

    if len(check_pay) != 0:
        for cp in check_pay:
            if cp['paid']:
                user_buy_services.append([cp['user_email'], cp['service_pk'], cp['service_name']])
                purchase_status += 1

    if purchase_status != 0:
        for service in user_buy_services:
            services = Services.objects.get(pk=service[1])
            service_price = int(services.service_price1) / 100 * int(services.service_price_procent)
            check_ref_service = UserReferalsService.objects.filter(user_email=check_pay[0]['user_email']).filter(
                service_price_prosent=service_price).filter(service_name=f"{check_pay[0]['service_name']}")
            if len(check_ref_service) == 0:
                ref_email = user.user_referal_email1
                name = ''
                if not ref_email == 'none':
                    ref_user_data = UsersProfile.objects.get(user_email=ref_email)
                    ref_user_data.user_balance += service_price
                    ref_user_data.user_referals_bonus += service_price
                    name = ref_user_data.user_name
                    ref_user_data.save()
                UserReferalsService(user_email=check_pay[0]['user_email'], user_name=name,
                                    service_price_prosent=service_price,
                                    service_name=f"{check_pay[0]['service_name']}", ref_email=ref_email).save()
            else:
                select_withdraw = UsersWithdraw.objects.filter(user_email=request.user.email)
                if len(select_withdraw) != 0:
                    data['withdraw_static'] = select_withdraw
                else:
                    data['withdraw_static'] = False

    if purchase_status != 0:
        UserReferalsService(user_email=check_pay[0]['user_email'], service_price_prosent=check_pay[0]['user_email'],
                            service_name=f"{check_pay[0]['service_name']}").save()
    if len(users_data) != 0:
        verify1 = users_data[0]['user_verify']
        user.user_verify = verify1
        user.save()
    if user.user_verify and user.user_balance >= configs[0]['withdraw_sum']:
        data['user_verify'] = True,
        data['user_verify2'] = True,

    if len(withdraws) != 0:
        if not withdraws[0]['paid']:
            data['withdraw_cash'] = withdraws[0]['user_balance'],
        else:
            data['withdraw_cash'] = '0'

    if request.method == 'POST':
        save_avatar(request, user.user_email)
    return render(request, 'cryptency/user_withdraws.html', context=data)


@login_required
def user_profile_withdraws_cash(request):
    user = UsersProfile.objects.get(user_email=request.user.email)
    users_data = UserSecureData.objects.filter(user_email=request.user.email).values()
    if len(users_data) != 0:
        verify1 = users_data[0]['user_verify']
        user.user_verify = verify1
        user.save()
    data = {
        'user_email': user.user_email,
        'user_referals_bonus': user.user_referals_bonus,
        'user_photo': user.user_photo,
        'user_name': user.user_name,
        'user_surname': user.user_surname,
        'user_balance': user.user_balance,
        'user_referals': user.user_referals,
        'ref_link': user.user_referals_link if user.user_referals_link != 'none' else 'none',
        'user_verify': True if user.user_verify else False,
        'user_reg_date': user.user_reg_date,
    }
    if request.method == 'POST':
        card_num = request.POST['card-num']
        UsersWithdraw(user_email=user.user_email, user_balance=user.user_balance, user_card_num=card_num).save()
        user.user_balance = 0
        user.save()
        return redirect('profile')
    if user.user_verify:
        return render(request, 'cryptency/withdraw_cash.html', context={'user_data': user})
    else:
        return redirect('profile')


@login_required
def user_profile_contacts(request):
    user = UsersProfile.objects.get(user_email=request.user)
    users_data = UserSecureData.objects.filter(user_email=request.user.email).values()
    if len(users_data) != 0:
        verify1 = users_data[0]['user_verify']
        user.user_verify = verify1
        user.save()
    data = {
        'user_email': user.user_email,
        'user_referals_bonus': user.user_referals_bonus,
        'user_photo': user.user_photo,
        'user_name': user.user_name,
        'user_surname': user.user_surname,
        'user_balance': user.user_balance,
        'user_referals': user.user_referals,
        'ref_link': user.user_referals_link if user.user_referals_link != 'none' else 'none',
        'user_verify': True if user.user_verify else False,
        'user_reg_date': user.user_reg_date,

    }
    if request.method == 'POST':
        save_avatar(request, user.user_email)
    return render(request, 'cryptency/contacts.html', context=data)


@login_required
def user_profile_videos(request):
    user = UsersProfile.objects.get(user_email=request.user)
    configs = AdminConfigs.objects.all()
    users_data = UserSecureData.objects.filter(user_email=request.user.email).values()
    if len(users_data) != 0:
        verify1 = users_data[0]['user_verify']
        user.user_verify = verify1
        user.save()
    data = {
        'user_email': user.user_email,
        'user_photo': user.user_photo,
        'user_name': user.user_name,
        'user_surname': user.user_surname,
        'user_balance': user.user_balance,
        'user_verify': True if user.user_verify else False,
        'ref_link': user.user_referals_link if user.user_referals_link != 'none' else 'none',
    }
    if request.method == 'POST':
        save_avatar(request, user.user_email)
    try:
        service_pks = []
        user_videos_data = []
        user2 = UsersPayChecks.objects.filter(user_email=request.user.email).values()
        if len(user2) != 0 and user2[0]['paid']:
            for pks in user2:
                service_pks.append(pks['service_pk'])
            for i in service_pks:
                user_videos = Videos.objects.filter(service_pk_id=i)
                if len(user_videos) != 0:
                    user_videos_data.append(user_videos)
            if len(user_videos_data) != 0:
                data['user_videos'] = user_videos_data
            else:
                data['status'] = 'Упс, нет видео роликов'

        elif user.user_service_id:
            pkid = int(str(user.user_service_id).split('-')[0])
            user_videos = Videos.objects.filter(user_service_id=pkid)
            if len(user_videos) != 0:
                user_videos_data.append(user_videos)
            if len(user_videos_data) != 0:
                data['user_videos'] = user_videos_data
                save_ref_link = UsersProfile.objects.get(user_email=request.user.email)
                if user.user_referals_link == 'none':
                    save_ref_link.user_referal_email1 = configs.ref_bonus1
                    insert_balance = UsersProfile.objects.get(user_email=save_ref_link.user_referal_email1)
                    insert_balance.user_balance = configs.ref_bonus1
                    insert_balance.user_referals_bonus = configs.ref_bonus1
                    save_ref_link.save()
                    return redirect('profile_videos')
        else:
            data['status'] = 'Упс, нет видео роликов'
    except Exception as ex:
        print(f'{type(ex).__name__}: {ex} | Line: {sys.exc_info()[-1].tb_lineno}')
        data['status'] = 'Упс, нет видео роликов'

    return render(request, 'cryptency/user_videos.html', context=data)


@login_required
def user_profile_settings(request):
    user = UsersProfile.objects.get(user_email=request.user)
    user_data = UserSecureData.objects.filter(user_email=request.user)
    users_data = UserSecureData.objects.filter(user_email=request.user.email).values()
    check_pay = UsersPayChecks.objects.filter(user_email=request.user.email).values()
    purchase_status = 0
    if len(check_pay) != 0:
        for cp in check_pay:
            if cp['paid']:
                purchase_status += 1
    if len(users_data) != 0:
        verify1 = users_data[0]['user_verify']
        user.user_verify = verify1
        user.save()
    if purchase_status != 0:
        UserReferalsService(user_email=check_pay[0]['user_email'], service_price_prosent=check_pay[0]['user_email'],
                            service_name=f"{check_pay[0]['service_name']}").save()
    data = {
        'user_email': user.user_email,
        'user_referals_bonus': user.user_referals_bonus,
        'user_photo': user.user_photo,
        'user_name': user.user_name,
        'user_surname': user.user_surname,
        'user_balance': user.user_balance,
        'user_referals': user.user_referals,
        'ref_link': user.user_referals_link if user.user_referals_link != 'none' else 'none',
        'user_verify': True if user.user_verify else False,
        'user_reg_date': user.user_reg_date,
        'user_data_verify': True if len(user_data) != 0 else False,

    }
    if request.method == 'POST':
        save_avatar(request, request.user.email)
        name = request.POST['name']
        surnname = request.POST['lastName']
        date = request.POST['date']
        user.user_name = name
        user.user_surname = surnname
        user.user_birthday = date
        user.save()
        return redirect('settings_profile')

    return render(request, 'cryptency/settings_profile.html', context=data)


@login_required
def user_profile_support(request):
    user = UsersProfile.objects.get(user_email=request.user)
    users_data = UserSecureData.objects.filter(user_email=request.user.email).values()
    if len(users_data) != 0:
        verify1 = users_data[0]['user_verify']
        user.user_verify = verify1
        user.save()
    data = {
        'user_email': user.user_email,
        'user_referals_bonus': user.user_referals_bonus,
        'user_photo': user.user_photo,
        'user_name': user.user_name,
        'user_surname': user.user_surname,
        'user_balance': user.user_balance,
        'user_referals': user.user_referals,
        'ref_link': user.user_referals_link if user.user_referals_link != 'none' else 'none',
        'user_verify': True if user.user_verify else False,
        'user_reg_date': user.user_reg_date,

    }
    if request.method == 'POST':
        save_avatar(request, user.user_email)
    return render(request, 'cryptency/user_support.html', context=data)


@login_required
def user_profile_purchase(request):
    user = UsersProfile.objects.get(user_email=request.user)
    services = Services.objects.all()
    wait_pay_check = UsersPayChecks.objects.filter(user_email=request.user.email).values()
    users_data = UserSecureData.objects.filter(user_email=request.user.email).values()
    pay_status = 0
    if len(wait_pay_check) != 0:
        for wpc in wait_pay_check:
            if not wpc['paid']:
                pay_status += 1
    if len(wait_pay_check) != 0:
        UserReferalsService(user_email=wait_pay_check[0]['user_email'],
                            service_price_prosent=wait_pay_check[0]['user_email'],
                            service_name=f"{wait_pay_check[0]['service_name']}").save()

    if len(users_data) != 0:
        verify1 = users_data[0]['user_verify']
        user.user_verify = verify1
        user.save()

    data = {
        'user_photo': user.user_photo,
        'user_name': user.user_name,
        'user_surname': user.user_surname,
        'user_balance': user.user_balance,
        'ref_link': user.user_referals_link if user.user_referals_link != 'none' else 'none',
        'services': services if len(services) != 0 else False,
        'pay_status': True if pay_status == 0 else False,
        'user_verify': True if user.user_verify else False,
    }
    if request.method == 'GET' and 'simbole' in request.GET:
        if request.GET['simbole'] == 'usd':
            return HttpResponse('usd')
        else:
            return HttpResponse('byn')

    if request.method == 'POST':
        save_avatar(request, user.user_email)
    return render(request, 'cryptency/user_purchase.html', context=data)


@login_required
def settings_secure(request):
    user = UsersProfile.objects.get(user_email=request.user)
    user_data = UserSecureData.objects.filter(user_email=request.user)
    users_data = UserSecureData.objects.filter(user_email=request.user.email).values()
    if len(users_data) != 0:
        verify1 = users_data[0]['user_verify']
        user.user_verify = verify1
        user.save()
    data = {
        'user_email': user.user_email,
        'user_referals_bonus': user.user_referals_bonus,
        'user_photo': user.user_photo,
        'user_name': user.user_name,
        'user_surname': user.user_surname,
        'user_balance': user.user_balance,
        'user_referals': user.user_referals,
        'ref_link': user.user_referals_link if user.user_referals_link != 'none' else 'none',
        'user_verify': True if user.user_verify else False,
        'user_reg_date': user.user_reg_date,
        'user_data_verify': True if len(user_data) != 0 else False,
    }

    if request.method == 'POST':
        save_avatar(request, user.user_email)
        try:
            pass1 = request.POST['password1']
            pass2 = request.POST['password2']
            user = UsersProfile.objects.get(user_email=request.user)
            user2 = User.objects.get(username=request.user)
            if user.user_password == pass1:
                user.user_password = pass2
                user2.set_password(pass2)
                user.save()
                user2.save()
                return render(request, 'cryptency/settings_secure.html',
                              context={'status': 'Пароль сохранен', 'status_color': 'success'})
            return render(request, 'cryptency/settings_secure.html',
                          context={'status': 'Пароли не совпадают', 'status_color': 'warning'})
        except Exception as ex:
            print(ex)
            redirect('/')

    if request.method == 'GET':
        if 'new_email' in request.GET:
            new_email = request.GET['new_email']
            user = UsersProfile.objects.filter(user_email=new_email).values()
            if len(user) != 0:
                return HttpResponse('incorrect')
            else:
                check_email = re.match(
                    "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$",
                    new_email)
                if check_email is None:
                    return HttpResponse('no_email')
                return HttpResponse('correct')
        elif 'email_code' in request.GET:
            email_code = request.GET['email_code']
            email_codes = UsersEmailVerifyTokens.objects.filter(user_token=email_code).values()
            if len(email_codes) == 0:
                return HttpResponse('incorrect')
            else:
                user = UsersProfile.objects.get(user_email=request.user.email)
                user2 = User.objects.get(username=request.user.email)
                user3 = UsersPayChecks.objects.get(user_email=request.user.email)
                user4 = UsersWithdraw.objects.get(user_email=request.user.email)
                user5 = UserReferalsService.objects.get(user_email=request.user.email)
                user.user_email = email_codes[0]['user_email']
                user2.email = email_codes[0]['user_email']
                user3.email = email_codes[0]['user_email']
                user4.email = email_codes[0]['user_email']
                user5.email = email_codes[0]['user_email']
                user.save()
                UsersEmailVerifyTokens.objects.get(user_token=email_code).delete()
                return HttpResponse('correct')

        elif 'send_code' in request.GET:
            token = secrets.token_hex(3)
            UsersEmailVerifyTokens(user_email=request.GET['email'], user_token=token).save()
            html = render_to_string(
                'cryptency/email_body.html',
                {'verify_url': token}
            )
            send_mail('Cryptency - подтверждение почты', 'Пожалуста подтвердите почту', settings.EMAIL_HOST_USER,
                      [request.user.email],
                      html_message=html,
                      fail_silently=True)
            return HttpResponse('send')

    return render(request, 'cryptency/settings_secure.html', context=data)


@login_required
def settings_document(request):
    user = UsersProfile.objects.get(user_email=request.user)
    user_data = UserSecureData.objects.filter(user_email=request.user)
    users_data = UserSecureData.objects.filter(user_email=request.user.email).values()
    if len(users_data) != 0:
        verify1 = users_data[0]['user_verify']
        user.user_verify = verify1
        user.save()
    data = {
        'user_email': user.user_email,
        'user_referals_bonus': user.user_referals_bonus,
        'user_photo': user.user_photo,
        'user_name': user.user_name,
        'user_surname': user.user_surname,
        'user_balance': user.user_balance,
        'user_referals': user.user_referals,
        'ref_link': user.user_referals_link if user.user_referals_link != 'none' else 'none',
        'user_verify': True if user.user_verify else False,
        'user_reg_date': user.user_reg_date,
        'user_data_verify': True if len(user_data) != 0 else False,
    }
    if request.method == 'POST':
        if 'avatar' in request.FILES:
            save_avatar(request, user.user_email)
        if request.FILES:
            seria = request.POST['seria']
            pass_num = request.POST['pass_num']
            pass_date_issue = request.POST['pass_date_issue']
            birthday = request.POST['birthday']
            user_email = request.user.email
            file_obj = request.FILES['pass_pic1']
            file_obj2 = request.FILES['pass_pic2']
            filename = f'users_pay_check/{user.user_email}_1.jpg'
            filename2 = f'users_pay_check/{user.user_email}_2.jpg'
            with default_storage.open(filename, 'wb+') as d:
                for chunk in file_obj.chunks():
                    d.write(chunk)
            with default_storage.open(filename2, 'wb+') as d:
                for chunk in file_obj2.chunks():
                    d.write(chunk)
            user = UserSecureData(
                user_email=user_email, user_pass_seria=seria, user_pass_num=pass_num,
                user_pass_date_issue=pass_date_issue, user_birthday=birthday,
                user_pass_photo1=filename, user_pass_photo2=filename2, user_name=user.user_name,
                user_surname=user.user_surname
            )
            user.save()
            return redirect('settings_docs')
    return render(request, 'cryptency/settings_document.html', context=data)


@login_required
def buy_service(request, pk):
    services = Services.objects.get(pk=pk)
    admin_configs = AdminConfigs.objects.all().values()
    data = {'services': services, 'card_number': admin_configs[0]['card_number']}
    if request.method == 'POST':
        if request.FILES:
            file_obj = request.FILES['pay_check']
            filename = f'users_pay_check/{request.user.email}.jpg'
            with default_storage.open(filename, 'wb+') as d:
                for chunk in file_obj.chunks():
                    d.write(chunk)

            user = UsersPayChecks(service_pk=pk, user_pay_check=filename, user_email=request.user.email,
                                  service_name=services.service_name)
            user.save()
            return redirect('user_purchase')

    return render(request, 'cryptency/buy_service.html', context=data)


def check_user_referal(request, ref_link):
    try:
        user = UsersProfile.objects.get(user_referals_link=f"{site_domen_link}/user_referal/{ref_link}")
        if user:
            user.user_referals += 1
            email = user.user_email
            user.save()
            return render(request, 'cryptency/signup.html', context={'is_ref': email})

    except Exception as ex:
        print(ex)
        return redirect('user_reg')

    if request.method == 'POST':
        return redirect('user_reg')


def email_verify(request, user_token):
    user_data = UsersEmailVerifyTokens.objects.filter(user_token=user_token).values()
    if user_data:
        try:
            user_email = user_data[0]['user_email']
            user_profile = UsersProfile.objects.get(user_email=user_email)
            user_token_data = UsersEmailVerifyTokens.objects.get(user_token=user_token)
            user_profile.user_email_verify = True
            user_profile.save()
            user_token_data.delete()
            # configs = AdminConfigs.objects.all().values()
            ref_user = UsersProfile.objects.get(user_email=request.user.email)
            ref_user2 = UsersProfile.objects.get(user_email=ref_user.user_referal_email1)
            ref_user2.user_referals += 1
            # ref_user2.user_referals_bonus += configs[0]['ref_bonus1']
            # ref_user2.user_balance += configs[0]['ref_bonus1']
            ref_user2.save()
        except:
            return redirect('user_login')
    return redirect('user_login')
