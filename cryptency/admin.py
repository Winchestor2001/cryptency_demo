from django.contrib import admin

from cryptency.models import *


class UsersPayChecksAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'service_name', 'service_pk', 'paid', 'user_pay_date', 'user_pay_check')


class ServicesAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'service_title', 'service_price1', 'service_price2')


class UsersProfileAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_email', 'user_balance', 'user_verify', 'user_reg_date', 'user_photo')


class AdminConfigsAdmin(admin.ModelAdmin):
    list_display = ('ref_bonus1', 'ref_bonus2', 'ref_bonus3', 'withdraw_sum', 'card_number')


class VideosAdmin(admin.ModelAdmin):
    list_display = ('video_title', 'service_pk')


admin.site.register(UsersProfile, UsersProfileAdmin)
admin.site.register(UsersEmailVerifyTokens)
admin.site.register(UserSecureData)
admin.site.register(Services, ServicesAdmin)
admin.site.register(UsersPayChecks, UsersPayChecksAdmin)
admin.site.register(Videos, VideosAdmin)
admin.site.register(AdminConfigs, AdminConfigsAdmin)
