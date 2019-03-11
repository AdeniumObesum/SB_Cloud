#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : tasks.py
# @Author: Clare
# @Date  : 2019/3/3 
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
# python manage.py celery worker -c 4 --loglevel=info   启动任务


from celery import task
from celery.schedules import crontab
from celery.task import periodic_task


@task
def async_task(job_name):
    """
    异步任务
    :param job_name:
    :return:
    """
    return 'some'


@periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
def get_time():
    """
    周期任务
    :return:
    """
