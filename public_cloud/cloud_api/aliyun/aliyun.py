#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : aliyun.py
# @Author: Clare
# @Date  : 2019/3/10 
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

import datetime
import json
import uuid
from collections import ChainMap

import requests

from public_cloud.cloud_api.aliyun import aliyun_util


class AliyunOperator(object):
    """
    阿里云api调用
    """

    def __init__(self, **kwargs):
        self.access_key = kwargs['access_key']
        self.secret_key = kwargs['secret_key']
        pass

    def request_2_aliyun(self, base_url, **kwargs):
        config = {
            'Format': 'JSON',
            'Version': '2014-05-26',
            'AccessKeyId': self.access_key,
            'SignatureMethod': 'HMAC-SHA1',
            'Timestamp': self.get_utc(),
            'SignatureVersion': '1.0',
            'SignatureNonce': str(uuid.uuid4()),
        }
        params = kwargs
        all_params = ChainMap(config, params)
        all_params = aliyun_util.get_signature(all_params=all_params, secret_key=self.secret_key)
        resp = requests.get(url=base_url, params=all_params)
        return json.loads(resp.content)

    def get_utc(self):
        UTCC = datetime.datetime.utcnow()
        utc_time = datetime.datetime.strftime(UTCC, "%Y-%m-%dT%H:%M:%SZ")
        return utc_time

    def api_get_region_info(self, endpoint='ecs.aliyuncs.com'):
        """
        获取地区信息
        :return:
        """
        base_url = 'https://' + endpoint
        action = 'DescribeRegions'
        params = {
            'Action': action
        }
        regions = self.request_2_aliyun(base_url=base_url, **params)
        return regions['Regions']['Region']
        # RegionId: cn-qingdao
        # RegionEndpoint: ecs.aliyuncs.com
        # LocalName: 华北1


# if __name__ == '__main__':
#     x = 'LTAIDICTHyLR9jsq'
#     y = 'jfYWdmsAf9qSjOmB7rEU9aewxyF38l'
#     a = AliyunOperator(access_key=x, secret_key=y)
#     b = a.api_get_region_info()
#     print(b)