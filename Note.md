# Django使用回忆录
*使用蓝鲸提供框架久了，便渐渐忘记了原汁原味的Django怎么用了，在公司做共有云管理系统时，做出的效果不能使自己满意，便计划自己再用原来的Django写一个出来，此篇文章记录Django2.1的配置和使用方法。以便以后查看。*

- settings.py的配置
```angular2html
1.静态文件

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]

2.使用mysql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sbcloud',
        'USER': 'root',
        'PASSWORD': '1997817',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

```
*遇到一些问题，在虚拟环境中执行pip install  --upgrade pip 后，pip报错：ImportError: cannot import name main。*
* 解决办法：重装了虚拟环境（实在无解）

*这时候运行项目报错：No module named 'MySQLdb'*
* 解决办法第一步：安装setuptools(若已安装则忽略)
    - 1.获取setuptools源码包，wget --no-check-certificate  https://pypi.python.org/packages/source/s/setuptools/setuptools-19.6.tar.gz
    - 2.解压进入解压后的包，执行 python3 setup.py build && sudo python3 setup.py install
* 解决办法第二步：安装pymysql，在py2中用的是MySQLdb，在py3中虽然换用pymysql，但是导入的包名依旧是原来的，所以我们需要改一下，在主项目目录下的init.py文件中添加两行：
    - import pymysql
    - pymysql.install_as_MySQLdb()
    
*至此Django应该可以正常跑起来啦～*

* 使用Django自带的用户认证系统,并重写字段
```cython
# 1.创建自己的user类
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, name, email, phone, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            name=name,
            email=UserManager.normalize_email(email),
            phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, phone, password=None):
        user = self.create_user(name, email, phone, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """重写user类"""
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    created_at = models.DateTimeField(verbose_name='注册日期', auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone = models.CharField(verbose_name='联系电话', max_length=100, blank=True, null=True)
    is_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ('email',)

    class Meta:
        ordering = ('-created_at',)

    def __unicode__(self):
        return self.name

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
```

