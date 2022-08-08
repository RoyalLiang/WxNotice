import time
import traceback
from urllib.parse import urlencode

import requests

from WeChatNotice.secure import WX_ACCESS_TOKEN_URL
from libs.enums import WxAccountStatusEnum
from libs.rdb import connect_redis
from WeChatNotice.settings import REDIS_HOST, REDIS_PORT, REDIS_PWD, REDIS_DB, REDIS_WX_ACCESS_TOKEN_PREFIX, \
    DEFAULT_SLEEP_TIME
from wx.models import WxAccountModel


class WxPubHandler:

    def __init__(self, r_host=REDIS_HOST, rp=REDIS_PORT, rdb=REDIS_DB, rpwd=REDIS_PWD, **kwargs):
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

    def get_access_token(self):
        while True:
            try:
                accounts = WxAccountModel.objects.filter(status=WxAccountStatusEnum.ACTIVE)
                for a in accounts:
                    self._get_account_access_token(a)
            except Exception:
                print(f"process error, msg: {traceback.format_exc()}")
            finally:
                time.sleep(DEFAULT_SLEEP_TIME)

    def _get_account_access_token(self, account):
        key = REDIS_WX_ACCESS_TOKEN_PREFIX + account.ename
        value = self.redis.get(key)
        if not value:
            self._request_to_wx(account, key)
        else:
            print('get access token success')

    def _request_to_wx(self, account, key):
        url = WX_ACCESS_TOKEN_URL + f'&{urlencode(dict(appid=account.app_id, secret=account.app_secret))}'
        r = requests.get(url)
        try:
            result = r.json()
            print(f'get result: {result}')
            if result.get('errcode'):
                print(f'error, code: {result["errcode"]}, msg: {result["errmsg"]}')
            else:
                self.redis.setex(key, result['expires_in'], result['access_token'])
        except Exception:
            print(traceback.format_exc())

    def verify_access_token(self):
        pass


wx_handler = WxPubHandler()
