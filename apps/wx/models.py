from django.db import models

# Create your models here.
from WeChatNotice.models import BaseModel


class WxAccountModel(BaseModel):

    STATUS = [
        (-1, '已失效'),
        (0, '待生效'),
        (1, '生效中'),
    ]

    name = models.CharField(max_length=50, null=False, db_index=True, verbose_name='账号名称')
    ename = models.CharField(max_length=50, null=False, db_index=True, default='', verbose_name='微信号')
    app_id = models.CharField(max_length=50, null=False, verbose_name='开发者ID')
    app_secret = models.CharField(max_length=150, null=False, default='', blank=True, verbose_name='开发者密钥')
    status = models.SmallIntegerField(choices=STATUS, db_index=True, default=0, verbose_name='启用状态')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'wx_account'
        verbose_name = '微信账号管理'
        verbose_name_plural = verbose_name
