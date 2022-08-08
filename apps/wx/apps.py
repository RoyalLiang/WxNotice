import threading

from django.apps import AppConfig


class WxConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wx'
    verbose_name = '微信公众账号管理'

    def ready(self):
        from wx.wx_handler import wx_handler
        thread = threading.Thread(target=wx_handler.get_access_token)
        thread.setDaemon(True)
        thread.start()
