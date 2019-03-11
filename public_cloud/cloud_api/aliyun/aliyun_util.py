#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : make_signature.py
# @Author: A.O.
# @Date  : 2018/9/12
# @license : Copyright(C), Nanyang Institute of Technology
# @Contact : 1837866781@qq.com
# @Software : PyCharm
# code is far away from bugs with the god animal protecting

__pet__ = '''   
              ┏┓     ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
'''

import base64
import datetime
import hmac
import sys
from hashlib import sha1
from urllib import parse


def timestrip():
    UTCC = datetime.datetime.utcnow()
    utcbefore5 = UTCC - datetime.timedelta(minutes=10)
    Endtime = datetime.datetime.strftime(UTCC, "%Y-%m-%dT%H:%M:%SZ")
    StartTime = datetime.datetime.strftime(utcbefore5, "%Y-%m-%dT%H:%M:%SZ")
    return StartTime, Endtime

def percent_encode(encodeStr):
    '''
    编码函数
    :param stri:
    :return:
    '''
    if isinstance(encodeStr, bytes):
        encodeStr = encodeStr.decode(sys.stdin.encoding)
    res = parse.quote_plus(encodeStr.encode('utf-8'), '')
    res = res.replace('+', '%20').replace('*', '%2A').replace('%7E', '~')
    return res


def get_signature(all_params,secret_key = ''):
    '''
    获取阿里api签名
    :param config:
    :param params:
    :return:
    '''
    # secret_key = 'oG4JoydUSCcs2hmRFFThIP9GmbPATR'  # 已开通公测
    # sometime, utc_now = timestrip()
    # config = {
    #     'Format': 'JSON',
    #     'Version': '2017-12-14',
    #     'AccessKeyId': 'LTAIy9vVmGyw7iap',
    #     'SignatureMethod': 'HMAC-SHA1',
    #     'Timestamp': utc_now,
    #     'SignatureVersion': '1.0',
    #     'SignatureNonce': str(uuid.uuid4()),
    # }
    # secret_key = 'jfYWdmsAf9qSjOmB7rEU9aewxyF38l'  # 贺阳的 没开通公测
    # sometime, utc_now = timestrip()
    # config = {
    #     'Format': 'JSON',
    #     'Version': '2017-12-14',
    #     'AccessKeyId': 'LTAIDICTHyLR9jsq',
    #     'SignatureMethod': 'HMAC-SHA1',
    #     'Timestamp': utc_now,
    #     'SignatureVersion': '1.0',
    #     'SignatureNonce': str(uuid.uuid4()),
    # }
    # params = {
    #     'Action': 'QueryAccountBalance',
    #     # 'BillingCycle': '2018-08'
    # }
    parameters = all_params
    sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
    canonicalizedQueryString = ''
    for (k, v) in sortedParameters:
        canonicalizedQueryString += '&' + percent_encode(k) + '=' + percent_encode(v)
    stringToSign = 'GET&%2F&' + percent_encode(canonicalizedQueryString[1:])  # 使用get请求方法
    bs = secret_key + '&'
    bs = bytes(bs, encoding='utf8')
    stringToSign = bytes(stringToSign, encoding='utf8')
    h = hmac.new(bs, stringToSign, sha1)
    # 进行编码
    signature = base64.b64encode(h.digest()).strip()
    all_params['Signature'] = signature
    return all_params



