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


class FirmSerializer(serializers.ModelSerializer):
    """
    云厂商序列化器
    """

    class Meta:
        model = models.FirmInfo
        fields = "__all__"


class HostInfoSerializer(serializers.ModelSerializer):
    """
    云主机序列化器
    """
    instance_type = serializers.SerializerMethodField()
    instance_status = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()
    instance_type_id = serializers.SerializerMethodField(method_name=None)
    instance_status_id = serializers.SerializerMethodField(method_name=None)
    class Meta:
        model = models.HostInfo
        fields = "__all__"

    def get_instance_type(self, obj):
        return obj.get_instance_type_display()

    def get_instance_status(self, obj):
        return obj.get_instance_status_display()

    def get_end_time(self, obj):
        return obj.end_time.strftime('%Y-%m-%d')

    def get_instance_type_id(self, obj):
        return obj.instance_type

    def get_instance_status_id(self, obj):
        return obj.instance_status