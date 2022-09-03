from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from cryptency.views import *

urlpatterns = [
    path('', home_page, name='home'),
    path('user_login/', user_login, name='user_login'),
    path('user_logout/', user_logout, name='user_logout'),
    path('user_reg/', user_reg, name='user_reg'),
    path('reset_password/', reset_password, name='reset_password'),
    path('profile/purchase/buy/<int:pk>', buy_service, name='buy_service'),
    path('profile/', user_profile, name='profile'),
    path('user_referal/<str:ref_link>', user_reg, name='check_user_referal'),
    path('auth/email_verify/<str:user_token>', email_verify, name='email_verify'),
    path('profile/accrual/', user_profile_accrual, name='profile_accrual'),
    path('profile/withdraws/', user_profile_withdraws, name='profile_withdraws'),
    path('profile/withdraws/cash', user_profile_withdraws_cash, name='withdraws_cash'),
    path('profile/contacts/', user_profile_contacts, name='profile_contacts'),
    path('profile/videos/', user_profile_videos, name='profile_videos'),
    path('profile/settings/profile_data', user_profile_settings, name='settings_profile'),
    path('profile/settings/secure/', settings_secure, name='settings_secure'),
    path('profile/settings/documents/', settings_document, name='settings_docs'),
    path('profile/support/', user_profile_support, name='profile_support'),
    path('profile/purchase/', user_profile_purchase, name='user_purchase'),
]
