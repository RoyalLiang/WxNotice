import time
import traceback
from urllib.parse import urlencode

import requests
from django.db import connection

from WeChatNotice.secure import WX_ACCESS_TOKEN_URL, WX_USER_LIST_URL, WX_USER_DETAIL_URL
from libs.enums import WxAccountStatusEnum
from libs.rdb import connect_redis
from WeChatNotice.settings import REDIS_HOST, REDIS_PORT, REDIS_PWD, REDIS_DB, REDIS_WX_ACCESS_TOKEN_PREFIX, \
    DEFAULT_SLEEP_TIME
from .wechat import wechat
from wx.models import WxAccountModel, WxPubAccountUserModel


class WxBaseHandler:

    def __init__(self, r_host=REDIS_HOST, rp=REDIS_PORT, rdb=REDIS_DB, rpwd=REDIS_PWD, **kwargs):
        self.acc = None
        self.r_host = r_host
        self.rp = rp
        self.rdb = rdb
        self.rpwd = rpwd
        self._gen_redis()

    def _gen_redis(self):
        if self.rpwd:
            self.redis = connect_redis(self.r_host, self.rp, self.rpwd, self.rdb)
        else:
            self.redis = connect_redis(self.r_host, self.rp, self.rdb)


class WxPubHandler(WxBaseHandler):

    def get_access_token(self):
        while True:
            try:
                accounts = WxAccountModel.objects.filter(status=WxAccountStatusEnum.ACTIVE)
                for a in accounts:
                    self._get_account_access_token(a)
                    user_handler.get_wx_users(a)
            except Exception:
                print(f"process error, msg: {traceback.format_exc()}")
            finally:
                connection.close()
                time.sleep(DEFAULT_SLEEP_TIME)

    def _get_account_access_token(self, account):
        key = REDIS_WX_ACCESS_TOKEN_PREFIX + account.ename
        value = self.redis.get(key)
        if not value:
            self._request_to_wx(account, key)
        else:
            print('get access token success')
            account.acc = value

    def _request_to_wx(self, account, key):
        params = dict(appid=account.app_id, secret=account.app_secret)
        r = wechat.get_acc_token(WX_ACCESS_TOKEN_URL, params)
        try:
            self.redis.setex(key, r['expires_in'], r['access_token'])
            account.acc = r['access_token']
        except Exception:
            print(traceback.format_exc())

    def verify_access_token(self):
        pass


class WxPubAccountUserHandler(WxBaseHandler):

    def get_wx_users(self, account):
        url = WX_USER_LIST_URL.format(account.app_id, '')
        r = requests.get(url)
        users = r.json()
        if err := users.get('errcode'):
            print(f'error, code: {err}, msg: {users["errmsg"]}')
        else:
            print(f'get users: {users}')
            for u in users['openid']:
                user_url = WX_USER_DETAIL_URL.format(self.acc, u)
                r = requests.get(user_url)
                user = r.json()
                self._process_user(account, user)

    @staticmethod
    def _process_user(account, user):
        WxPubAccountUserModel.save_or_update(account, user)


wx_handler = WxPubHandler()
user_handler = WxPubAccountUserHandler()
