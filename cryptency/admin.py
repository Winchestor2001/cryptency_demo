from django.contrib import admin

from cryptency.models import *


class UsersPayChecksAdmin(admin.ModelAdmin):
    search_fields = ['user_email', 'user_pay_date', 'service_name']
    list_display = ('user_email', 'service_name', 'service_pk', 'paid', 'user_pay_date', 'user_pay_check')


class ServicesAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'service_title', 'service_price1', 'service_price2', 'service_price_procent')


class UsersProfileAdmin(admin.ModelAdmin):
    search_fields = ['user_email', 'user_pay_date', 'service_name', 'user_name', 'user_verify']
    list_display = ('user_name', 'user_email', 'user_balance', 'user_verify', 'user_reg_date', 'user_photo')


class AdminConfigsAdmin(admin.ModelAdmin):
    list_display = ('ref_bonus1', 'ref_bonus2', 'ref_bonus3', 'withdraw_sum', 'card_number')


class VideosAdmin(admin.ModelAdmin):
    list_display = ('video_title', 'service_pk_id')


class UsersWithdrawAdmin(admin.ModelAdmin):
    search_fields = ['user_email', 'user_card_num']
    list_display = ('user_email', 'user_balance', 'user_card_num', 'paid', 'user_withdraw_date')


class UserReferalsServiceAdmin(admin.ModelAdmin):
    search_fields = ['user_email', 'service_price_prosent', 'service_bougth_date']
    list_display = ('user_email', 'user_name', 'service_price_prosent', 'service_name', 'ref_email', 'service_bougth_date')


admin.site.register(UsersProfile, UsersProfileAdmin)
admin.site.register(UsersWithdraw, UsersWithdrawAdmin)
admin.site.register(UsersEmailVerifyTokens)
admin.site.register(UserSecureData)
admin.site.register(Services, ServicesAdmin)
admin.site.register(UsersPayChecks, UsersPayChecksAdmin)
admin.site.register(Videos, VideosAdmin)
admin.site.register(AdminConfigs, AdminConfigsAdmin)
admin.site.register(UserReferalsService, UserReferalsServiceAdmin)
