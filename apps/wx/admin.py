from django.contrib import admin

# Register your models here.
from wx.models import WxAccountModel


@admin.register(WxAccountModel)
class WxAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'app_id', 'app_secret', 'category', 'status', 'create_time']
