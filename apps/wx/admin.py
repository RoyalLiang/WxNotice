from django.contrib import admin

# Register your models here.
from wx.models import WxAccountModel, WxPubAccountUserModel, WxPubAccountTemplateModel


@admin.register(WxAccountModel)
class WxAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'app_id', 'app_secret', 'category', 'status', 'create_time']

    list_filter = ['category', 'status']


@admin.register(WxPubAccountUserModel)
class WxPubAccountUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'pub_account', 'open_id', 'subscribe_scene', 'subscribe_time', 'remark']
