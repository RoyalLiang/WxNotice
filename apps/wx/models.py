from django.db import models

# Create your models here.
from libs.models import BaseModel
from libs.utils import timestamp2datetime
from wx.hardcode import WX_USER_FIELDS_MAPPING


class WxAccountModel(BaseModel):

    STATUS = [
        (-1, '已失效'),
        (0, '待生效'),
        (1, '生效中'),
    ]

    CATEGORY = [
        (0, '未注明'),
        (1, '订阅号未认证'),
        (2, '订阅号已认证'),
        (3, '服务号未认证'),
        (4, '服务号已认证')
    ]

    name = models.CharField(max_length=50, null=False, db_index=True, verbose_name='账号名称')
    ename = models.CharField(max_length=50, null=False, db_index=True, default='', verbose_name='微信号')
    category = models.SmallIntegerField(default=0, choices=CATEGORY, verbose_name='账号类别')
    app_id = models.CharField(max_length=50, null=False, verbose_name='开发者ID')
    app_secret = models.CharField(max_length=150, null=False, default='', blank=True, verbose_name='开发者密钥')
    status = models.SmallIntegerField(choices=STATUS, db_index=True, default=0, verbose_name='启用状态')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'wx_account'
        verbose_name = '微信账号管理'
        verbose_name_plural = verbose_name


class WxPubAccountTemplateModel(BaseModel):
    pub_account = models.ForeignKey(
        WxAccountModel, db_constraint=False, related_name='templates', on_delete=models.CASCADE, verbose_name='所属公众号'
    )
    tid = models.CharField(max_length=150, db_index=True, null=False, verbose_name='模板ID')
    primary_industry = models.CharField(max_length=100, verbose_name='一级行业')
    deputy_industry = models.CharField(max_length=100, verbose_name='二级行业')
    title = models.CharField(max_length=100, verbose_name='模板标题')
    content = models.CharField(max_length=100, verbose_name='模板内容')

    class Meta:
        db_table = 'wx_account_template'
        verbose_name = '消息模板管理'
        verbose_name_plural = verbose_name


class WxPubAccountUserModel(BaseModel):

    STATUS = [
        (0, '已取关'),
        (1, '已关注')
    ]

    pub_account = models.ForeignKey(
        WxAccountModel, db_constraint=False, related_name='users', on_delete=models.CASCADE, verbose_name='所属公众号'
    )
    open_id = models.CharField(max_length=150, db_index=True, verbose_name='OpenID')
    union_id = models.CharField(max_length=150, db_index=True, verbose_name='union_id')
    gender = models.SmallIntegerField(default=-1, verbose_name='性别')
    subscribe_time = models.DateTimeField(null=True, default='', verbose_name='订阅时间')
    remark = models.CharField(max_length=100, null=True, default='', verbose_name='备注')
    subscribe_scene = models.CharField(max_length=100, db_index=True, default='', verbose_name='关注来源')
    status = models.SmallIntegerField(choices=STATUS, verbose_name='关注状态')

    class Meta:
        db_table = 'wx_account_user'
        verbose_name = '公众号用户管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.pub_account.name}-{self.open_id}'

    @classmethod
    def save_or_update(cls, account, data):
        body = cls.trans_fields(data, WX_USER_FIELDS_MAPPING)
        cls._trans_fields(body)
        user = cls.objects.update_or_create(pub_account=account, open_id=body['open_id'], defaults=body)

    @staticmethod
    def _trans_fields(data):
        if data.get('subscribe_time'):
            data['subscribe_time'] = timestamp2datetime(data['subscribe_time'])


class WxSendMessageUserModel(BaseModel):

    STATUS = [
        (0, '待生效'),
        (1, '生效中'),
    ]

    pub_account = models.ForeignKey(
        WxPubAccountUserModel, db_constraint=False, related_name='msg_users', on_delete=models.CASCADE, verbose_name='所属公众号'
    )
    open_id = models.CharField(max_length=100, db_index=True, verbose_name='唯一标识')
    message_type = models.CharField(max_length=100, default='', blank=True, verbose_name='消息类型，空表示全类型')
    start_time = models.DateTimeField(verbose_name='发送时间')
    loop_num = models.SmallIntegerField(default=0, verbose_name='循环次数，0表示无限循环')
    status = models.SmallIntegerField(choices=STATUS, db_index=True, default=0, verbose_name='启用状态')

    class Meta:
        db_table = 'wx_account_message_user'
        verbose_name = '发信用户管理'
        verbose_name_plural = verbose_name


