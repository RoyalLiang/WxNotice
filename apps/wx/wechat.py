import traceback
from urllib.parse import urlencode

import requests


class WeChatPubApi:

    @staticmethod
    def _group_url(url, params):
        if params:
            url += f'?{urlencode(params)}'

    def _send_request(self, url, method='get', params=None, body=None, **kwargs):
        try:
            self._group_url(url, params)
            if body:
                result = getattr(requests, method)(url=url, json=body)
            else:
                result = getattr(requests, method)(url=url)
            return self._parse_result(result)
        except:
            print(f"request error, msg: {traceback.format_exc()}")
            return {}

    def _parse_result(self, result):
        result = result.json()
        if err := result.get('errcode'):
            if err == '40001':
                self._fresh_acc_token()
                return
            else:
                print(f'error, code: {err}, msg: {result["errmsg"]}')
                return
        else:
            return result

    def _fresh_acc_token(self):
        pass

    def get_acc_token(self, url, params=None, body=None):
        result = self._send_request(url, params, body)
        return result

    def verify_acc_token(self):
        pass

    def get_pub_templates(self):
        pass

    def get_pub_users(self):
        pass

    def get_pub_user_info(self):
        pass


wechat = WeChatPubApi()
