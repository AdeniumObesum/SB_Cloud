#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Clare
import base64
import hashlib
import hmac

secret_id = "AKID1qPilY9MQLF2cxPxb1C9rOm7KI1TjCQi"
secret_key = "HI3gEeoiMkuqY1FI7h3B6nQzQdcMq5BD"


def get_string_to_sign(method, endpoint, params):
    s = method + endpoint + "/?"
    query_str = "&".join("%s=%s" % (k, params[k]) for k in sorted(params))
    return s + query_str


def sign_str(key, s, method):
    hmac_str = hmac.new(key.encode("utf8"), s.encode("utf8"), method).digest()
    return base64.b64encode(hmac_str)


def get_signature(all_params={}, end_point='', secret_key=''):
    s = get_string_to_sign('GET', end_point, all_params)
    all_params['Signature'] = sign_str(secret_key, s, hashlib.sha1)
    return all_params


from collections import ChainMap
import requests
import time
import random
import json

if __name__ == '__main__':
    url = "https://cvm.tencentcloudapi.com"
    action = 'DescribeRegions'
    end_pint = "cvm.tencentcloudapi.com"
    config = {
        'Action': action,
        'SecretId': secret_id,
        'Timestamp': int(time.time()),
        'Nonce': random.randint(0, 1000000),
        'SignatureMethod': 'HmacSHA1',
        'Version': '2017-03-12'
    }
    action_params = {

    }
    params = ChainMap(config, action_params)
    all_params = get_signature(all_params=params, end_point=end_pint, secret_key=secret_key)
    resp = requests.get(url=url, params=all_params)
    data = json.loads(resp.content)
    print(data)
