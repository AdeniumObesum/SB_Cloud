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
# 同步地区
# 同步主机
# 同步磁盘

class AliyunOperator(object):
    """
    阿里云api调用
    """

    def __init__(self, **kwargs):
        self.access_key = kwargs['access_key']
        self.secret_key = kwargs['secret_key']
        self.firm = models.FirmInfo.objects.filter(firm_key=100)[0]
        try:
            self.account = models.AccountInfo.objects.filter(firm_key=100, access_key=self.access_key)[0]
        except Exception as e:
            self.account = None
        pass

    def get_date_time(self, string):  ###获取datetime
        get_time = re.findall('(\d+\-\d+\-\d+)|(\d+\:\d+)', string)
        format_time = get_time[0][0] + ' ' + get_time[1][1]
        return datetime.datetime.strptime(format_time, '%Y-%m-%d %H:%M')

    def request_2_aliyun(self, base_url, response_pages=[], **kwargs):  # 返回所有请求页
        config = {
            'Format': 'JSON',
            'Version': '2014-05-26',
            'AccessKeyId': self.access_key,
            'SignatureMethod': 'HMAC-SHA1',
            'Timestamp': self.get_utc(),
            'SignatureVersion': '1.0',
            'SignatureNonce': str(uuid.uuid4()),
            'PageSize': '20'
        }
        params = kwargs
        all_params = ChainMap(config, params)
        all_params = aliyun_util.get_signature(all_params=all_params, secret_key=self.secret_key)
        resp = requests.get(url=base_url, params=all_params)
        resp = json.loads(resp.content)
        response_pages.append(resp)
        # print(resp)
        if 'PageSize' in resp:
            if int(resp['TotalCount'])/int(resp['PageSize']) > int(resp['PageNumber']):
                config['PageNumber'] = str(int(resp['PageNumber']) + 1)
                self.request_2_aliyun(base_url=base_url, **config, response_pages=response_pages)
        return response_pages

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
            'Action': action,
        }
        response_list = []
        regions_pages = self.request_2_aliyun(base_url=base_url, **params)
        for one_page in regions_pages:
            response_list += one_page['Regions']['Region']
        return response_list
        # RegionId: cn-qingdao
        # RegionEndpoint: ecs.aliyuncs.com
        # LocalName: 华北1

    def api_get_region_info_to_model(self):
        '''
        先执行这个初始化地区信息
        :return:
        '''
        regions = self.api_get_region_info()
        db_all_info = models.RegionInfo.objects.filter(firm_key=self.firm.firm_key, region_type=0, is_delete=0)
        api_region_list = [i['RegionId'] for i in regions]

        for info in db_all_info:
            if info.region_id not in api_region_list:
                info.is_delete = 1
                info.save()

        for region in regions:
            models.RegionInfo.objects.update_or_create(
                region_id=region['RegionId'],
                firm_key=self.firm.firm_key,
                is_delete=0,
                defaults={
                    # 'firm_key': self.firm.firm_key,
                    # 'region_id': region['RegionId'],
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
        regions = models.RegionInfo.objects.filter(firm_key=self.firm.firm_key, is_delete=0)
        params = {
            'Action': 'DescribeInstances',
        }
        base_url = 'https://ecs.aliyuncs.com'
        response_list = []
        for region in regions:
            params['RegionId'] = region.region_id
            ecs_pages = self.request_2_aliyun(base_url=base_url, **params)
            for one_page in ecs_pages:
                print(one_page)
                response_list += one_page['Instances']['Instance']
        return response_list

    def api_get_ecs_to_model(self):
        """
        同步数据库
        :return:
        """
        ecs_list = self.api_get_ecs()
        db_all_info = models.HostInfo.objects.filter(account_id=self.account.id)
        api_ecs_list = [i['InstanceId'] for i in ecs_list]

        for info in db_all_info:
            if info.instance_id not in api_ecs_list:
                info.is_delete = 1
                info.save()

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
            region = models.RegionInfo.objects.get(region_id=ecs['RegionId'], is_delete=0, firm_key=self.firm.firm_key)
            models.HostInfo.objects.update_or_create(
                account_id=self.account.id,
                instance_id=ecs['InstanceId'],
                defaults={
                    # 'account_id': self.account.id,
                    # 'instance_id': ecs['InstanceId'],
                    'instance_name': ecs['HostName'],
                    'os_name': ecs['OSName'],
                    'instance_type': instance_type,
                    'instance_status': instance_status,
                    'instance_pub_ip': ecs['PublicIpAddress']['IpAddress'][0],
                    'instance_pri_ip': ecs['InnerIpAddress']['IpAddress'][0] if ecs['InnerIpAddress']['IpAddress'] else ecs['VpcAttributes']['PrivateIpAddress']['IpAddress'][0],
                    'instance_vpc_ip': ecs['VpcAttributes']['PrivateIpAddress']['IpAddress'][0] if ecs['VpcAttributes']['PrivateIpAddress']['IpAddress'] else '',
                    'network_interface_id': ecs['NetworkInterfaces']['NetworkInterface'][0]['NetworkInterfaceId'],
                    'internet_charge_type': internet_charge_type,
                    'instance_charge_type': instance_charge_type,
                    'price_per_hour': ecs['SpotPriceLimit'],
                    'region_id': region.id,
                    'is_overdue': is_overdue,
                    'start_time': self.get_date_time(ecs['CreationTime']),
                    'end_time': self.get_date_time(ecs['ExpiredTime']),
                    'is_delete': 0,
                }
            )

    def api_get_disks(self):
        regions = models.RegionInfo.objects.filter(firm_key=self.firm.firm_key)
        base_url = 'https://ecs.aliyuncs.com'
        params = {
            'Action': 'DescribeDisks'
        }
        response_list = []
        for region in regions:
            params['RegionId'] = region.region_id
            disks_pages = self.request_2_aliyun(base_url=base_url, **params)
            for one_page in disks_pages:
                response_list += one_page['Disks']['Disk']
        return response_list
        pass

    def api_get_disks_to_model(self):
        disks = self.api_get_disks()
        db_all_info = models.DiskInfo.objects.filter(firm_key=self.firm.firm_key, account_id=self.account.id,
                                                     is_delete=0)
        api_disk_list = [i['DiskId'] for i in disks]

        for info in db_all_info:
            if info.disk_id not in api_disk_list:
                info.is_delete = 1
                info.save()

        for disk in disks:

            if disk['Type'] == 'data':
                disk_type = 1
            elif disk['Type'] == 'system':
                disk_type = 0

            if disk['Category'] == 'cloud':
                disk_category = 0
            elif disk['Category'] == 'cloud_efficiency':
                disk_category = 1
            elif disk['Category'] == 'cloud_ssd':
                disk_category = 2
            elif disk['Category'] == 'ephemeral_ssd':
                disk_category = 3
            elif disk['Category'] == 'cloud_essd':
                disk_category = 4

            if disk['Status'] == 'In_use':
                disk_status = 0
            elif disk['Status'] == 'Available':
                disk_status = 1
            elif disk['Status'] == 'Attaching':
                disk_status = 2
            elif disk['Status'] == 'Detaching':
                disk_status = 3
            elif disk['Status'] == 'Creating':
                disk_status = 4
            elif disk['Status'] == 'Relniting':
                disk_status = 5

            if disk['DiskChargeType'] == 'PrePaid':
                disk_charge_type = 0
            elif disk['DiskChargeType'] == 'PostPaid':
                disk_charge_type = 1

            region = models.RegionInfo.objects.get(region_id=disk['RegionId'], is_delete=0, firm_key=self.firm.firm_key)
            instance = models.HostInfo.objects.get(is_delete=0, instance_id=disk['InstanceId'],
                                                   account_id=self.account.id)

            models.DiskInfo.objects.update_or_create(
                account_id=self.account.id,
                disk_id=disk['DiskId'],
                is_delete=0,
                defaults={
                    # account_id: self.account.id,
                    'region_id': region.id,
                    'disk_type': disk_type,
                    'instance_id': instance.id,
                    'disk_name': disk['DiskName'],
                    'disk_category': disk_category,
                    'encrypted': disk['Encrypted'],
                    'disk_size': disk['Size'],
                    'disk_status': disk_status,
                    'disk_charge_type': disk_charge_type
                }
            )

            ### 存

# if __name__ == '__main__':
#     x = 'LTAIDICTHyLR9jsq'
#     y = 'jfYWdmsAf9qSjOmB7rEU9aewxyF38l'
#     a = AliyunOperator(access_key=x, secret_key=y)
#     a.api_get_ecs()
