from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class UserProfile(models.Model):
    '''用户信息表'''

    user = models.OneToOneField(User,on_delete=models.CASCADE)  # 与django作对应
    email = models.EmailField(verbose_name='邮箱', max_length=100)
    phone = models.CharField(verbose_name='联系电话', max_length=100)
    create_time = models.DateTimeField(verbose_name='注册日期',)

    pass
