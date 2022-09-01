import json
import random
import secrets

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from django_cryptency import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from .models import UsersProfile, UsersEmailVerifyTokens, Services, UserSecureData, UsersPayChecks, Videos, AdminConfigs

# site_domen_link = 'http://127.0.0.1:8000'
site_domen_link = 'http://cryptency.pythonanywhere.com'


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
        services = Services.objects.all()
        return render(request, 'cryptency/user_profile.html', context={'services': services})
    logout(request)
    return HttpResponseRedirect('/')


def user_reg(request, ref_link=None):
    context = {}
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
            configs = AdminConfigs.objects.all().values()
            ref_user.user_referals += 1
            ref_user.user_referals_bonus += configs[0]['ref_bonus1']
            ref_user.save()
            reg = UsersProfile(user=usr, user_name=name, user_surname=surname, user_email=email, user_password=pwd,
                               user_country=country, user_referal_email1=is_ref, user_referals_link=f'{site_domen_link}/user_referal/{token}')
        else:
            reg = UsersProfile(user=usr, user_name=name, user_surname=surname, user_email=email, user_password=pwd,
                               user_country=country, user_referals_link=f'{site_domen_link}/user_referal/{token}')
        UsersEmailVerifyTokens(user_email=email, user_token=token).save()
        reg.sert_id = "%05i" % (usr.id,)
        reg.save()
        context['status'] = 'Пожалуста подтвердите почту'
        html = render_to_string(
            'cryptency/email_body.html',
            {'verify_url': f'{site_domen_link}/auth/email_verify/{token}'}
        )
        send_mail('Cryptency - подтверждение почты', 'Пожалуста подтвердите почту', settings.EMAIL_HOST_USER, [email],
                  html_message=html,
                  fail_silently=True)
        return render(request, 'cryptency/signup.html', context=context)

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
                    context['status'] = 'Почта или пароль не правельный'
            else:
                context['status'] = 'Ваша почта не подтверждена'
        except Exception as ex:
            print(ex)
            context['status'] = 'Это почта не зарегистрирована'
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
    check_pay = UsersPayChecks.objects.filter(user_email=request.user.email)
    purchase_status = 0
    if len(check_pay) != 0:
        for cp in check_pay:
            if cp.paid:
                purchase_status += 1
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
        'purchase_status': True if purchase_status != 0 else False
    }
    if request.method == 'POST':
        save_avatar(request, request.user.email)
        return redirect('profile')
    return render(request, 'cryptency/user_profile.html', context=data)


@login_required
def user_profile_accrual(request):
    user = UsersProfile.objects.get(user_email=request.user)
    token = secrets.token_hex(15)
    data = {
        'user_email': user.user_email,
        'user_referals_bonus': user.user_referals_bonus,
        'user_photo': user.user_photo,
        'user_name': user.user_name,
        'user_surname': user.user_surname,
        'user_balance': user.user_balance,
        'user_referals': user.user_referals,
        'ref_link': user.user_referals_link if user.user_referals_link != 'none' else 'none',
        'user_verify': 'Верифицирован' if user.user_verify else None,
        'user_reg_date': user.user_reg_date,

    }
    if request.method == 'POST':
        save_avatar(request, request.user.email)
    return render(request, 'cryptency/user_accrual.html', context=data)


@login_required
def user_profile_withdraws(request):
    user = UsersProfile.objects.get(user_email=request.user)
    token = secrets.token_hex(15)
    data = {
        'user_email': user.user_email,
        'user_referals_bonus': user.user_referals_bonus,
        'user_photo': user.user_photo,
        'user_name': user.user_name,
        'user_surname': user.user_surname,
        'user_balance': user.user_balance,
        'user_referals': user.user_referals,
        'ref_link': user.user_referals_link if user.user_referals_link != 'none' else 'none',
        'user_verify': 'Верифицирован' if user.user_verify else None,
        'user_reg_date': user.user_reg_date,

    }
    if request.method == 'POST':
        save_avatar(request, user.user_email)
    return render(request, 'cryptency/user_withdraws.html', context=data)


@login_required
def user_profile_contacts(request):
    user = UsersProfile.objects.get(user_email=request.user)
    token = secrets.token_hex(15)
    data = {
        'user_email': user.user_email,
        'user_referals_bonus': user.user_referals_bonus,
        'user_photo': user.user_photo,
        'user_name': user.user_name,
        'user_surname': user.user_surname,
        'user_balance': user.user_balance,
        'user_referals': user.user_referals,
        'ref_link': user.user_referals_link if user.user_referals_link != 'none' else 'none',
        'user_verify': 'Верифицирован' if user.user_verify else None,
        'user_reg_date': user.user_reg_date,

    }
    if request.method == 'POST':
        save_avatar(request, user.user_email)
    return render(request, 'cryptency/contacts.html', context=data)


@login_required
def user_profile_videos(request):
    user = UsersProfile.objects.get(user_email=request.user)
    token = secrets.token_hex(15)
    configs = AdminConfigs.objects.all()
    data = {
        'user_email': user.user_email,
        'user_photo': user.user_photo,
        'user_name': user.user_name,
        'user_surname': user.user_surname,
        'user_balance': user.user_balance,
        'ref_link': user.user_referals_link if user.user_referals_link != 'none' else 'none',

    }
    if request.method == 'POST':
        save_avatar(request, user.user_email)
    try:
        service_pks = []
        user_videos_data = []
        user2 = UsersPayChecks.objects.filter(user_email=request.user.email)
        if len(user2) != 0:
            for pks in user2:
                service_pks.append(pks.service_pk)
        for i in service_pks:
            user_videos = Videos.objects.filter(service_pk=i)
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
        print(ex)
        data['status'] = 'Упс, нет видео роликов'

    return render(request, 'cryptency/user_videos.html', context=data)


@login_required
def user_profile_settings(request):
    user = UsersProfile.objects.get(user_email=request.user)
    token = secrets.token_hex(15)
    data = {
        'user_email': user.user_email,
        'user_referals_bonus': user.user_referals_bonus,
        'user_photo': user.user_photo,
        'user_name': user.user_name,
        'user_surname': user.user_surname,
        'user_balance': user.user_balance,
        'user_referals': user.user_referals,
        'ref_link': user.user_referals_link if user.user_referals_link != 'none' else 'none',
        'user_verify': user.user_verify,
        'user_reg_date': user.user_reg_date,

    }
    if request.method == 'POST':
        save_avatar(request, request.user.email)
    return render(request, 'cryptency/settings_profile.html', context=data)


@login_required
def user_profile_support(request):
    user = UsersProfile.objects.get(user_email=request.user)
    token = secrets.token_hex(15)
    data = {
        'user_email': user.user_email,
        'user_referals_bonus': user.user_referals_bonus,
        'user_photo': user.user_photo,
        'user_name': user.user_name,
        'user_surname': user.user_surname,
        'user_balance': user.user_balance,
        'user_referals': user.user_referals,
        'ref_link': user.user_referals_link if user.user_referals_link != 'none' else 'none',
        'user_verify': 'Верифицирован' if user.user_verify else None,
        'user_reg_date': user.user_reg_date,

    }
    if request.method == 'POST':
        save_avatar(request, user.user_email)
    return render(request, 'cryptency/user_support.html', context=data)


@login_required
def user_profile_purchase(request):
    user = UsersProfile.objects.get(user_email=request.user)
    token = secrets.token_hex(15)
    services = Services.objects.all()
    wait_pay_check = UsersPayChecks.objects.filter(user_email=request.user.email).values()
    pay_status = 0
    if len(wait_pay_check) != 0:
        for wpc in wait_pay_check:
            if not wpc['paid']:
                pay_status += 1

    data = {
        'user_photo': user.user_photo,
        'user_name': user.user_name,
        'user_surname': user.user_surname,
        'user_balance': user.user_balance,
        'ref_link': user.user_referals_link if user.user_referals_link != 'none' else 'none',
        'services': services if len(services) != 0 else False,
        'pay_status': True if pay_status == 0 else False,
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
    token = secrets.token_hex(15)
    data = {
        'user_email': user.user_email,
        'user_referals_bonus': user.user_referals_bonus,
        'user_photo': user.user_photo,
        'user_name': user.user_name,
        'user_surname': user.user_surname,
        'user_balance': user.user_balance,
        'user_referals': user.user_referals,
        'ref_link': user.user_referals_link if user.user_referals_link != 'none' else 'none',
        'user_verify': 'Верифицирован' if user.user_verify else None,
        'user_reg_date': user.user_reg_date,

    }

    if request.method == 'POST':
        save_avatar(request, user.user_email)
        try:
            pass1 = request.POST['password1']
            pass2 = request.POST['password2']
            user = UsersProfile.objects.get(user_email=request.user)
            user2 = User.objects.get(username=request.user)
            print(user.user_password, pass1)
            if user.user_password == pass1:
                user.user_password = pass2
                user2.set_password(pass2)
                user.save()
                user2.save()
                return render(request, 'cryptency/settings_secure.html',
                              context={'status': 'Пароль сохранен', 'status_color': 'success'})
            return render(request, 'cryptency/settings_secure.html',
                          context={'status': 'Пароль не совпадает', 'status_color': 'warning'})
        except Exception as ex:
            print(ex)
            redirect('/')
    return render(request, 'cryptency/settings_secure.html', context=data)


@login_required
def settings_document(request):
    user = UsersProfile.objects.get(user_email=request.user)
    token = secrets.token_hex(15)
    data = {
        'user_email': user.user_email,
        'user_referals_bonus': user.user_referals_bonus,
        'user_photo': user.user_photo,
        'user_name': user.user_name,
        'user_surname': user.user_surname,
        'user_balance': user.user_balance,
        'user_referals': user.user_referals,
        'ref_link': user.user_referals_link if user.user_referals_link != 'none' else 'none',
        'user_verify': 'Верифицирован' if user.user_verify else None,
        'user_reg_date': user.user_reg_date,

    }
    if request.method == 'POST':
        if 'avatar' in request.FILES:
            save_avatar(request, user.user_email)
        if request.FILES:
            seria = request.POST['seria']
            pass_num = request.POST['pass_num']
            pass_date_issue = request.POST['pass_date_issue']
            departmen_code = request.POST['departmen_code']
            place_of_birth = request.POST['place_of_birth']
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
                user_pass_date_issue=pass_date_issue, user_departmen_code=departmen_code,
                user_place_of_birth=place_of_birth, user_birthday=birthday,
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
            return redirect('profile')

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
        user_email = user_data[0]['user_email']
        user_profile = UsersProfile.objects.get(user_email=user_email)
        user_token_data = UsersEmailVerifyTokens.objects.get(user_token=user_token)
        user_profile.user_email_verify = True
        user_profile.save()
        user_token_data.delete()

        return redirect('user_login')
