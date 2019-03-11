#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : serializers.py
# @Author: Clare
# @Date  : 2019/3/7 
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
from rest_framework import serializers

from myauth import models as auth_models
from public_cloud import models


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    注册序列器
    """

    class Meta:
        model = auth_models.User
        fields = "__all__"


class FamilySerializer(serializers.ModelSerializer):
    """
    家族表序列器
    """

    class Meta:
        model = models.Family
        fields = "__all__"
