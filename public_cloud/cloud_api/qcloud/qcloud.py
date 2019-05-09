#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : qcloud.py
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
import random
import re
import time
from collections import ChainMap
from math import ceil

import requests

from public_cloud import models
from public_cloud.cloud_api.qcloud import qcloud_util


# 先初始化云厂商
# 再录入家族
# 再录入账户
# 同步地区
# 同步主机
# 同步磁盘

class QcloudOperator(object):
    """
    腾讯云api调用
    """

    def __init__(self, **kwargs):
        self.access_key = kwargs['access_key']
        self.secret_key = kwargs['secret_key']
        self.firm = models.FirmInfo.objects.filter(firm_key=101)[0]
        try:
            self.account = models.AccountInfo.objects.filter(firm_key=101, access_key=self.access_key)[0]
        except Exception as e:
            self.account = None
        pass

    def get_date_time(self, string):  # ## 获取datetime
        get_time = re.findall('(\d+\-\d+\-\d+)|(\d+\:\d+)', string)
        format_time = get_time[0][0] + ' ' + get_time[1][1]
        return datetime.datetime.strptime(format_time, '%Y-%m-%d %H:%M')


    def request_2_qcloud(self, base_url, end_point, config={}, params={}):  # 返回所有请求页
        response_pages = []
        all_params = ChainMap(config, params)
        all_params = qcloud_util.get_signature(all_params=all_params, end_point=end_point, secret_key=self.secret_key)
        resp = requests.get(url=base_url, params=all_params, headers={'Connection':'close'})
        resp = json.loads(resp.content)
        response_pages.append(resp['Response'])
        # print(all_params)
        # print(resp)
        offset = 0
        limit = 20
        if 'TotalCount' in resp['Response']:
            if int(resp['Response']['TotalCount']) > 20:
                pages = ceil(int(resp['Response']['TotalCount']) / 20)
                for page in range(2, pages):
                    # 每页一次请求，这里不用递归
                    offset += 20
                    config['Offset'] = offset
                    config['Limit'] = limit
                    all_params = ChainMap(config, params)
                    all_params = qcloud_util.get_signature(all_params=all_params, end_point=end_point,
                                                           secret_key=self.secret_key)
                    resp = requests.get(url=base_url, params=all_params)
                    resp = json.loads(resp.content)
                    response_pages.append(resp['Response'])
        return response_pages

    def get_utc(self):
        UTCC = datetime.datetime.utcnow()
        utc_time = datetime.datetime.strftime(UTCC, "%Y-%m-%dT%H:%M:%SZ")
        return utc_time

    def api_get_region_info(self, endpoint='cvm.tencentcloudapi.com'):
        """
        获取地区信息
        :return:
        """
        base_url = 'https://' + endpoint
        action = 'DescribeRegions'
        config = {
            'Action': action,
            'SecretId': self.access_key,
            'Timestamp': int(time.time()),
            'Nonce': random.randint(0, 1000000),
            'SignatureMethod': 'HmacSHA1',
            'Version': '2017-03-12'
        }
        params = {

        }
        response_list = []
        regions_pages = self.request_2_qcloud(base_url=base_url, end_point=endpoint, config=config, params=params)
        for one_page in regions_pages:
            response_list += one_page['RegionSet']
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
        api_region_list = [i['Region'] for i in regions]

        for info in db_all_info:
            if info.region_id not in api_region_list:
                info.is_delete = 1
                info.save()

        for region in regions:
            models.RegionInfo.objects.update_or_create(
                region_id=region['Region'],
                firm_key=self.firm.firm_key,
                is_delete=0,
                defaults={
                    'region_type': 0,
                    'region_name': region['RegionName'],
                    'end_point': ''
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

        base_url = 'https://cvm.tencentcloudapi.com'
        response_list = []
        for region in regions:
            config = {
                'SecretId': self.access_key,
                'Timestamp': int(time.time()),
                'Nonce': random.randint(0, 1000000),
                'SignatureMethod': 'HmacSHA1',
                'Version': '2017-03-12',
                'Offset': 0,
                'Limit': 20
            }
            params['Region'] = region.region_id
            ecs_pages = self.request_2_qcloud(base_url=base_url, end_point='cvm.tencentcloudapi.com', config=config,
                                              params=params)
            # print(ecs_pages)
            for one_page in ecs_pages:
                # print(one_page)
                for index in range(0, len(one_page['InstanceSet'])):
                    one_page['InstanceSet'][index]['RegionId'] = region.region_id
                response_list += one_page['InstanceSet']
        return response_list

    def api_get_ecs_to_model(self):
        """
        同步数据库
        :return:
        """
        ecs_list = self.api_get_ecs()
        # print(ecs_list)
        db_all_info = models.HostInfo.objects.filter(account_id=self.account.id, is_import=1)
        not_imports = models.HostInfo.objects.filter(account_id=self.account.id, is_import=0)
        not_imports_list = [i.instance_id for i in not_imports]
        api_ecs_list = []
        api_ecs_list_to_model = []
        for i in ecs_list:
            if (i['InstanceId'] not in not_imports_list):
                api_ecs_list.append(i['InstanceId'])
                api_ecs_list_to_model.append(i)
        for info in db_all_info:
            if info.instance_id not in api_ecs_list:
                info.is_delete = 1
                info.save()

        for ecs in api_ecs_list_to_model:
            if 'CentOS' in ecs['OsName']:
                instance_type = 0
            elif 'Window' in ecs['OsName']:
                instance_type = 1

            if ecs['InstanceState'] == 'RUNNING':
                instance_status = 0
            elif ecs['Status'] == 'STARTING':
                instance_status = 1
            elif ecs['Status'] == 'STOPPING':
                instance_status = 2
            elif ecs['Status'] == 'STOPPED':
                instance_status = 3

            if ecs['InternetAccessible']['InternetChargeType'] == 'TRAFFIC_POSTPAID_BY_HOUR' == 'BANDWIDTH_PACKAGE':
                internet_charge_type = 0
            elif ecs['InternetAccessible']['InternetChargeType'] == 'BANDWIDTH_PREPAID' or ecs['InternetAccessible'][
                'InternetChargeType'] or ecs['InternetAccessible'][
                'InternetChargeType'] == 'BANDWIDTH_POSTPAID_BY_HOUR':
                internet_charge_type = 1

            if ecs['InstanceChargeType'] == 'PREPAID':
                instance_charge_type = 0
            elif ecs['InstanceChargeType'] == 'POSTPAID_BY_HOUR':
                instance_charge_type = 1

            # #### 到这了

            region = models.RegionInfo.objects.get(region_id=ecs['RegionId'], is_delete=0, firm_key=self.firm.firm_key)
            models.HostInfo.objects.update_or_create(
                account_id=self.account.id,
                instance_id=ecs['InstanceId'],
                defaults={
                    'instance_name': ecs['InstanceName'],
                    'os_name': ecs['OsName'],
                    'instance_type': instance_type,
                    'instance_status': instance_status,
                    'instance_pub_ip': ecs['PublicIpAddresses'][0],
                    'instance_pri_ip': ecs['PrivateIpAddresses'][0],
                    'instance_vpc_ip': '',
                    'network_interface_id': ecs['VirtualPrivateCloud']['SubnetId'],
                    'internet_charge_type': internet_charge_type,
                    'instance_charge_type': instance_charge_type,
                    'price_per_hour': 0,
                    'region_id': region.id,
                    'is_overdue': 0,
                    'start_time': self.get_date_time(ecs['CreatedTime']),
                    'end_time': self.get_date_time(ecs['ExpiredTime']),
                    'is_delete': 0,
                }
            )
            self.api_get_instance_disks_to_model(instance_id=ecs['InstanceId'], region_id=ecs['RegionId'])

    def api_get_instance_disks(self, instance_id, region_id):
        print('获取磁盘', instance_id)
        end_point = 'cbs.tencentcloudapi.com'
        base_url = 'https://cbs.tencentcloudapi.com'
        params = {
            'Action': 'DescribeDisks',
        }
        response_list = []
        if instance_id and region_id:
            config = {
                'SecretId': self.access_key,
                'Timestamp': int(time.time()),
                'Nonce': random.randint(0, 1000000),
                'SignatureMethod': 'HmacSHA1',
                'Version': '2017-03-12',
                'Offset': 0,
                'Limit': 20
            }
            params['Filters.0.Name'] = 'instance-id'
            params['Filters.0.Values.0'] = instance_id
            params['Region'] = region_id
            disks_pages = self.request_2_qcloud(base_url=base_url, end_point=end_point, config=config, params=params)
            # print(params)
            print(disks_pages)
            for one_page in disks_pages:
                # print(one_page)
                for index in range(0, len(one_page['DiskSet'])):
                    one_page['DiskSet'][index]['RegionId'] = region_id
                response_list += one_page['DiskSet']
        else:
            regions = models.RegionInfo.objects.filter(firm_key=self.firm.firm_key, is_delete=0)
            for region in regions:
                config = {
                    'SecretId': self.access_key,
                    'Timestamp': int(time.time()),
                    'Nonce': random.randint(0, 1000000),
                    'SignatureMethod': 'HmacSHA1',
                    'Version': '2017-03-12',
                    'Offset': 0,
                    'Limit': 20
                }
                params['Region'] = region.region_id
                disks_pages = self.request_2_qcloud(base_url=base_url, end_point=end_point, config=config,
                                                    params=params)
                for one_page in disks_pages:
                    response_list += one_page['DiskSet']
                    print(one_page)
        # print('================',response_list)
        return response_list

    def api_get_instance_disks_to_model(self, instance_id=None, region_id=None):
        disks = self.api_get_instance_disks(instance_id=instance_id, region_id=region_id)
        instance = models.HostInfo.objects.filter(instance_id=instance_id)
        if instance:
            db_all_info = models.DiskInfo.objects.filter(account_id=self.account.id, instance_id=instance[0].id,
                                                         is_delete=0)
        else:
            db_all_info = models.DiskInfo.objects.filter(account_id=self.account.id, is_delete=0)
        api_disk_list = [i['DiskId'] for i in disks]
        for info in db_all_info:
            if info.disk_id not in api_disk_list:
                info.is_delete = 1
                info.save()

        for disk in disks:

            if disk['DiskUsage'] == 'DATA_DISK':
                disk_type = 1
            elif disk['DiskUsage'] == 'SYSTEM_DISK':
                disk_type = 0

            if disk['DiskType'] == 'CLOUD_BASIC':
                disk_category = 0
            elif disk['DiskType'] == 'CLOUD_PREMIUM':
                disk_category = 1
            elif disk['DiskType'] == 'CLOUD_SSD':
                disk_category = 2

            if disk['DiskState'] == 'ATTACHED':
                disk_status = 0
            elif disk['DiskState'] == 'UNATTACHED':
                disk_status = 1
            elif disk['DiskState'] == 'ATTACHING':
                disk_status = 2
            elif disk['DiskState'] == 'DETACHING':
                disk_status = 3
            else:
                disk_status = 5

            if disk['DiskChargeType'] == 'PREPAID':
                disk_charge_type = 0
            elif disk['DiskChargeType'] == 'POSTPAID_BY_HOUR':
                disk_charge_type = 1

            region = models.RegionInfo.objects.get(region_id=region_id, is_delete=0, firm_key=self.firm.firm_key)
            instance = models.HostInfo.objects.get(is_delete=0, instance_id=disk['InstanceId'],
                                                   account_id=self.account.id)

            models.DiskInfo.objects.update_or_create(
                account_id=self.account.id,
                disk_id=disk['DiskId'],
                defaults={
                    # account_id: self.account.id,
                    'region_id': region.id,
                    'disk_type': disk_type,
                    'instance_id': instance.id,
                    'disk_name': disk['DiskName'],
                    'disk_category': disk_category,
                    'encrypted': disk['Encrypt'],
                    'disk_size': disk['DiskSize'],
                    'disk_status': disk_status,
                    'disk_charge_type': disk_charge_type,
                    'is_delete': 0
                }
            )
            self.api_get_snapshots_to_model(disk_id=disk['DiskId'], region_id=disk['RegionId'],
                                            instance_id=disk['InstanceId'])

            #  ## 存

    def api_get_snapshots(self, disk_id=None, region_id=None):
        base_url = 'https://cbs.tencentcloudapi.com'
        end_point = 'cbs.tencentcloudapi.com'
        params = {
            'Action': 'DescribeSnapshots'
        }
        config = {
            'SecretId': self.access_key,
            'Timestamp': int(time.time()),
            'Nonce': random.randint(0, 1000000),
            'SignatureMethod': 'HmacSHA1',
            'Version': '2017-03-12',
            'Offset': 0,
            'Limit': 20
        }
        response_list = []
        if disk_id and region_id:
            params['Region'] = region_id
            params['Filters.0.Name'] = 'disk-id'
            params['Filters.0.Values.0'] = disk_id
            snapshot_pages = self.request_2_qcloud(base_url=base_url, end_point=end_point, config=config, params=params)
            # print(snapshot_pages)
            for one_page in snapshot_pages:
                print(one_page)
                # print(one_page['Snapshots']['Snapshot'])
                response_list += one_page['SnapshotSet']
        else:
            snapshot_pages = self.request_2_qcloud(base_url=base_url, end_point=end_point, config=config, params=params)
            for one_page in snapshot_pages:
                # print(one_page)
                response_list += one_page['SnapshotSet']
        return response_list

    def api_get_snapshots_to_model(self, disk_id=None, region_id=None, instance_id=None):
        snapshot_list = self.api_get_snapshots(disk_id=disk_id, region_id=region_id)
        disk = models.DiskInfo.objects.get(disk_id=disk_id, account_id=self.account.id, is_delete=0)
        db_all_info = models.SnapshotInfo.objects.filter(account_id=self.account.id, disk_id=disk.id)
        api_snapshot_list = [i['SnapshotId'] for i in snapshot_list]

        for info in db_all_info:
            if info.snapshot_id not in api_snapshot_list:
                info.is_delete = 1
                info.save()

        for snapshot in snapshot_list:

            region = models.RegionInfo.objects.get(region_id=region_id, is_delete=0, firm_key=self.firm.firm_key)
            instance = models.HostInfo.objects.get(is_delete=0, instance_id=instance_id,
                                                   account_id=self.account.id)

            if snapshot['Percent'] == 100:
                available_status = 0
            else:
                available_status = 1

            if snapshot['SnapshotState'] == 'NORMAL':
                snapshot_status = 0
            elif snapshot['SnapshotState'] == 'CREATING' or snapshot['SnapshotState'] == 'ROLLBACKING':
                snapshot_status = 1
            else:
                snapshot_status = 2

            create_time = self.get_date_time(snapshot['CreateTime'])
            if not snapshot['IsPermanent']:
                dead_time = self.get_date_time(snapshot['DeadlineTime'])
                days = (dead_time - create_time).days
            else:
                days = 9999

            models.SnapshotInfo.objects.update_or_create(
                account_id=self.account.id,
                snapshot_id=snapshot['SnapshotId'],
                defaults={
                    'region_id': region.id,
                    'instance_id': instance.id,
                    'available_status': available_status,
                    'disk_id': disk.id,
                    'snapshot_name': snapshot['SnapshotName'],
                    'snapshot_progress': snapshot['Percent'],
                    'retention_days': days,
                    'snapshot_status': snapshot_status,
                    'source_disk_size': snapshot['DiskSize'],
                    # 'create_time': self.get_date_time(snapshot['CreationTime']),
                    'snapshot_create_time': create_time,
                    'is_delete': 0,
                }
            )

    def api_stop_instance(self, instance_id, force_stop=False):
        """关机"""
        base_url = 'https://cvm.tencentcloudapi.com'
        end_point = 'cvm.tencentcloudapi.com'
        instance = models.HostInfo.objects.get(instance_id=instance_id, is_delete=0)
        region = models.RegionInfo.objects.get(firm_key=self.firm.firm_key, id=instance.region_id)
        if force_stop:
            force_str = 'TRUE'
        else:
            force_str = 'FALSE'
        params = {
            'Action': 'StopInstances',
            'InstanceIds.0': instance_id,
            'Region': region.region_id,
            'ForceStop': force_str
        }
        config = {
            'SecretId': self.access_key,
            'Timestamp': int(time.time()),
            'Nonce': random.randint(0, 1000000),
            'SignatureMethod': 'HmacSHA1',
            'Version': '2017-03-12',
        }
        data = {
            'code': 0,
            'msg': ''
        }
        resp = self.request_2_qcloud(base_url=base_url, end_point=end_point, config=config, params=params)
        if (len(resp[0]) == 1):
            data['msg'] = '已关机'
        else:
            data['code'] = 1
            data['msg'] = resp[0]['Error']['Message']
        return data

    def api_start_instance(self, instance_id):
        base_url = 'https://cvm.tencentcloudapi.com'
        end_point = 'cvm.tencentcloudapi.com'
        instance = models.HostInfo.objects.get(instance_id=instance_id, is_delete=0)
        region = models.RegionInfo.objects.get(firm_key=self.firm.firm_key, id=instance.region_id)
        params = {
            'Action': 'StartInstances',
            'InstanceIds.0': instance_id,
            'Region': region.region_id
        }
        config = {
            'SecretId': self.access_key,
            'Timestamp': int(time.time()),
            'Nonce': random.randint(0, 1000000),
            'SignatureMethod': 'HmacSHA1',
            'Version': '2017-03-12',
        }
        data = {
            'code': 0,
            'msg': ''
        }
        resp = self.request_2_qcloud(base_url=base_url, end_point=end_point, config=config, params=params)
        if (len(resp[0]) == 1):
            data['msg'] = '已开机'
        else:
            data['code'] = 1
            data['msg'] = resp[0]['Error']['Message']
        return data
        pass

    def api_delete_snapshot(self, force=False, snapshot_id=None):
        '''
        删除快照
        :return:
        '''
        base_url = 'https://cbs.tencentcloudapi.com'
        end_point = 'cbs.tencentcloudapi.com'
        snapshot = models.SnapshotInfo.objects.get(snapshot_id=snapshot_id, is_delete=0)
        region = models.RegionInfo.objects.get(firm_key=self.firm.firm_key, id=snapshot.region_id)
        data = {
            'code': 0,
            'msg': ''
        }

        if snapshot_id:
            params = {
                'Action': 'DeleteSnapshots',
                'SnapshotIds.0': snapshot_id,
                'Region': region.region_id
                # 'Force': force_str
            }
            config = {
                'SecretId': self.access_key,
                'Timestamp': int(time.time()),
                'Nonce': random.randint(0, 1000000),
                'SignatureMethod': 'HmacSHA1',
                'Version': '2017-03-12',
            }

            resp = self.request_2_qcloud(base_url=base_url, end_point=end_point, config=config, params=params)
            print(resp)
            if 'flowId' in resp[0]:
                data['msg'] = '执行成功'
                models.SnapshotInfo.objects.filter(is_delete=0, account_id=self.account.id,
                                                   snapshot_id=snapshot_id).update(is_delete=0)
            else:
                data['code'] = 1
                data['msg'] = resp[0]['Error']['Message']
            return data

    def api_create_snapshot(self, snapshot_name=None, disk_id=None, description=None):
        """
        创建快照
        :param snapshot_name:
        :return:
        """
        base_url = 'https://cbs.tencentcloudapi.com'
        end_point = 'cbs.tencentcloudapi.com'
        disk = models.DiskInfo.objects.get(disk_id=disk_id, is_delete=0)
        region = models.RegionInfo.objects.get(firm_key=self.firm.firm_key, id=disk.region_id)
        data = {
            'code': 0,
            'msg': '',
            'data': {}
        }
        params = {
            'Action': 'CreateSnapshot',
            'Region': region.region_id,
            'DiskId': disk_id,
            'SnapshotName': snapshot_name
            # 'Description': description
        }
        config = {
            'SecretId': self.access_key,
            'Timestamp': int(time.time()),
            'Nonce': random.randint(0, 1000000),
            'SignatureMethod': 'HmacSHA1',
            'Version': '2017-03-12',
        }

        resp = self.request_2_qcloud(base_url=base_url, end_point=end_point, config=config, params=params)
        if "SnapshotId" in resp[0]:
            data['msg'] = '执行成功'
            data['data']['snapshot_id'] = resp[0]['SnapshotId']
            instance = models.HostInfo.objects.get(id=disk.instance_id)
            time.sleep(10)
            self.api_get_snapshots_to_model(disk_id=disk_id, region_id=region.region_id, instance_id=instance.instance_id)
        else:
            data['code'] = 1
            data['msg'] = resp[0]['Error']['Message']

        return data

    def api_rollback_snapshot(self, disk_id, snapshot_id):
        """
        恢复快照
        :return:
        """
        base_url = 'https://cbs.tencentcloudapi.com'
        end_point = 'cbs.tencentcloudapi.com'
        action = 'ApplySnapshot'
        disk = models.DiskInfo.objects.get(id=disk_id, is_delete=0)
        region = models.RegionInfo.objects.get(firm_key=self.firm.firm_key, id=disk.region_id)
        data = {
            'code': 0,
            'msg': '',
            'data': {}
        }
        params = {
            'Action': action,
            'DiskId': disk.disk_id,
            'SnapshotId': snapshot_id,
            'Region': region.region_id
        }
        config = {
            'SecretId': self.access_key,
            'Timestamp': int(time.time()),
            'Nonce': random.randint(0, 1000000),
            'SignatureMethod': 'HmacSHA1',
            'Version': '2017-03-12',
        }

        instance = models.HostInfo.objects.filter(id=disk.instance_id, is_delete=0)
        if disk.disk_status == 0:  # 磁盘使用中
            if instance[0].instance_status == 3:  # 实例已停止
                try:
                    resp = self.request_2_qcloud(base_url=base_url, end_point=end_point, config=config, params=params)
                    print(resp)
                    if len(resp[0]) == 1:  # 一个requestId
                        data['msg'] = '快照恢复中'
                    else:
                        data['code'] = 1
                        data['msg'] = resp[0]['Error']['Message']

                except Exception as e:
                    data['code'] = 1
                    data['msg'] = 'something error: %s' % e
            else:
                data['code'] = 1
                data['msg'] = '实例未停止，无法恢复快照'
        else:
            data['code'] = 1
            data['msg'] = '磁盘不是“使用中”状态，无法恢复快照'
        return data
        pass

# if __name__ == '__main__':
#     x = 'LTAIDICTHyLR9jsq'
#     y = 'jfYWdmsAf9qSjOmB7rEU9aewxyF38l'
#     a = AliyunOperator(access_key=x, secret_key=y)
#     a.api_get_ecs()
