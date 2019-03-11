#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Clare
import base64
import hashlib
import hmac

secret_id = "AKIDz8krbsJ5yKBZQpn74WFkmLPx3EXAMPLE"
secret_key = "Gu5t9xGARNpq86cd98joQYCN3EXAMPLE"


def get_string_to_sign(method, endpoint, params):
    s = method + endpoint + "/?"
    query_str = "&".join("%s=%s" % (k, params[k]) for k in sorted(params))
    return s + query_str


def sign_str(key, s, method):
    hmac_str = hmac.new(key.encode("utf8"), s.encode("utf8"), method).digest()
    return base64.b64encode(hmac_str)


def get_signature(config={}, params={}, end_point='', secret_key=''):
    all_params = dict(config.items() + params.items())
    s = get_string_to_sign('GET', end_point, all_params)
    all_params['Signature'] = sign_str(secret_key, s, hashlib.sha1)
    return all_params
