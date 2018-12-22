from django.db import models
from myauth import models as my_model
from SBCloudManager import settings


# Create your models here.

class FirmInfo(models.Model):
    """
    云厂商信息表
    """
    us_name = models.CharField('英文名', max_length=100, unique=True)
    zh_name = models.CharField('中文名', max_length=200)
    # 0: 未导入   1：已导入
    is_import = models.IntegerField('是否已导入用户', default=0)
    # 0: 未开发   1：已开发
    is_dev = models.IntegerField('是否开发', default=0)

    class Meta:
        verbose_name = '云厂商信息表'
        db_table = 'firm'


class AccountInfo(models.Model):
    """
    云账户信息表
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    firm = models.ForeignKey('FirmInfo', on_delete=models.CASCADE)
    access_key = models.CharField('accessKey', max_length=100, null=True)
    secret_key = models.CharField('secretKey', max_length=100, null=True)
    create_at = models.DateTimeField('账户录入日期', auto_now_add=True)
    is_delete = models.BooleanField('是否删除', default=False)

    class Meta:
        verbose_name = '账户信息表'
        db_table = 'account'
