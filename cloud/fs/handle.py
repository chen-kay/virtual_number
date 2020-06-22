import requests

from cloud.fs.settings import fs_settings
from cloud.fs.utils import encry_sign

_SIGN_KEY = fs_settings.SIGN_KEY
_SIGN_URI = fs_settings.SIGN_URI


def get_call_mobile(dest):
    '''获取呼叫号码
    '''
    try:
        sign_keys = {'cust_id': dest, 'key': _SIGN_KEY}
        params = {'cust_id': dest, 'sign': encry_sign(sign_keys)}
        res = requests.get(url=_SIGN_URI, params=params)
        if res.status_code == 200:
            data = res.json()
            print(data)
            return data['data']
        return None
    except Exception as e:
        print(e)
        return None
