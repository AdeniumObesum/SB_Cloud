#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : CloudDic.py
# @Author: Clare
# @Date  : 2019/3/19 
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

from public_cloud.cloud_api.aliyun.aliyun import AliyunOperator
from public_cloud.cloud_api.qcloud.qcloud import QcloudOperator

CloudDic = {
    '100': AliyunOperator,
    '101': QcloudOperator
}