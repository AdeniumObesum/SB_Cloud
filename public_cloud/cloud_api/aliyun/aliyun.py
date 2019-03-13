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
import re
import uuid
from collections import ChainMap

import requests

from public_cloud import models
from public_cloud.cloud_api.aliyun import aliyun_util


# 先初始化云厂商
# 再录入家族
# 再录入账户

class AliyunOperator(object):
    """
    阿里云api调用
    """

    def __init__(self, **kwargs):
        self.access_key = kwargs['access_key']
        self.secret_key = kwargs['secret_key']
        self.firm = models.FirmInfo.objects.filter(us_name='aliyun')[0]
        self.account = models.AccountInfo.objects.filter(firm_id=self.firm.id, access_key=self.access_key)[0]
        pass

    def get_date_time(self, string):  ###获取datetime
        get_time = re.findall('(\d+\-\d+\-\d+)|(\d+\:\d+)', string)
        format_time = get_time[0][0] + ' ' + get_time[1][1]
        return datetime.datetime.strptime(format_time, '%Y-%m-%d %H:%M')

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

    def api_get_region_info_to_model(self):

        regions = self.api_get_region_info()
        for region in regions:
            models.RegionInfo.objects.update_or_create(
                region_id=region['RegionId'],
                defaults={
                    'firm_id': self.firm.id,
                    'region_id': region['RegionId'],
                    'region_type': 0,
                    'region_name': region['LocalName'],
                    'end_point': region['RegionEndpoint']
                }
            )

    def api_get_ecs(self):
        """
        获取实例
        :return:
        """
        regions = models.RegionInfo.objects.filter(firm_id=self.firm.id)
        params = {
            'Action': 'DescribeInstances',
        }
        base_url = 'https://ecs.aliyuncs.com'
        response_list = []
        for region in regions:
            params['RegionId'] = region.region_id
            response = self.request_2_aliyun(base_url=base_url, **params)
            response_list += response['Instances']['Instance']
        return response_list

    def api_get_ecs_to_model(self):
        """
        同步数据库
        :return:
        """
        ecs_list = self.api_get_ecs()
        for ecs in ecs_list:
            if ecs['OSType'] == 'linux':
                instance_type = 0
            elif ecs['OSType'] == 'windows':
                instance_type = 1

            if ecs['Status'] == 'Running':
                instance_status = 0
            elif ecs['Status'] == 'Starting':
                instance_status = 1
            elif ecs['Status'] == 'Stopping':
                instance_status = 2
            elif ecs['Status'] == 'Stopped':
                instance_status = 3

            if ecs['InternetChargeType'] == 'PayByTraffic':
                internet_charge_type = 0
            elif ecs['InternetChargeType'] == 'PayByBandwidth':
                internet_charge_type = 1

            if ecs['InstanceChargeType'] == 'PrePaid':
                instance_charge_type = 0
            elif ecs['InstanceChargeType'] == 'PostPaid':
                instance_charge_type = 1

            if len(ecs['OperationLocks']['LockReason']) > 0:
                is_overdue = 2
            else:
                is_overdue = 0
            models.HostInfo.objects.update_or_create(
                account_id=self.account.id,
                instance_id=ecs['InstanceId'],
                defaults={
                    'instance_name': ecs['HostName'],
                    'os_name': ecs['OSName'],
                    'instance_type': instance_type,
                    'instance_status': instance_status,
                    'instance_pub_ip': ecs['PublicIpAddress']['IpAddress'][0],
                    'instance_pri_ip': ecs['InnerIpAddress']['IpAddress'][0],
                    'instance_vpc_ip': ecs['VpcAttributes']['PrivateIpAddress']['IpAddress'][0],
                    'network_interface_id': ecs['NetworkInterfaces']['NetworkInterface']['MacAddress'],
                    'internet_charge_type': internet_charge_type,
                    'instance_charge_type': instance_charge_type,
                    'price_per_hour': ecs['SpotPriceLimit'],
                    'region_id': ecs['RegionId'],
                    'is_overdue': is_overdue,
                    'start_time': self.get_date_time(ecs['CreationTime']),
                    'end_time': self.get_date_time(ecs['ExpiredTime'])
                }
            )

# if __name__ == '__main__':
#     x = 'LTAIDICTHyLR9jsq'
#     y = 'jfYWdmsAf9qSjOmB7rEU9aewxyF38l'
#     a = AliyunOperator(access_key=x, secret_key=y)
#     a.api_get_ecs()
