import datetime

from django.db import models


# Create your models here.

class FirmInfo(models.Model):
    """
    云厂商信息表
    """

    firm_key = models.IntegerField(verbose_name='云厂商代码')
    us_name = models.CharField('英文名', max_length=100, unique=True)
    icon_name = models.CharField('图标名', max_length=100, null=True)
    zh_name = models.CharField('中文名', max_length=200)

    # # 0: 未导入   1：已导入
    # is_import = models.IntegerField('是否已导入用户', default=0)
    # # 0: 未开发   1：已开发
    # is_dev = models.IntegerField('是否开发', default=0)

    class Meta:
        verbose_name = '云厂商信息表'
        db_table = 'firm'


# class Menu(models.Model):
#     """
#     左侧菜单
#     """
#     name = models.CharField(verbose_name='菜单名', max_length=100)
#     url = models.CharField(verbose_name='菜单路径', max_length=200)
#     parent_id = models.IntegerField(verbose_name='父亲菜单', default=0)
#     is_delete = models.IntegerField(default=0)
#
#     class Meta:
#         verbose_name = '菜单表'
#         db_table = 'Menu'


class Family(models.Model):
    """
    家族
    """
    user_id = models.CharField(verbose_name='外键id', max_length=100)
    user_email = models.CharField(verbose_name='用户邮箱', max_length=100)
    family_name = models.CharField(verbose_name='家族名', max_length=100)

    # family_type_choices = (
    #     (0, 'common'),
    #     (1, 'noble'),
    # )
    # family_type = models.IntegerField(verbose_name='家族类型', choices=family_type_choices, default=0)

    class Meta:
        verbose_name = '用户家族表'
        db_table = 'family'


class AccountInfo(models.Model):
    """
    云账户信息表
    """
    firm_id = models.IntegerField(verbose_name='云厂商id')
    family_id = models.IntegerField(verbose_name='家族id')
    access_key = models.CharField('accessKey', max_length=100, null=True)
    secret_key = models.CharField('secretKey', max_length=100, null=True)
    account_status = models.IntegerField(verbose_name='账户状态', default=0)
    app_id = models.CharField('appid', max_length=100, null=True)
    create_at = models.DateTimeField('账户录入日期', auto_now_add=True)
    is_delete = models.IntegerField(verbose_name='是否删除', default=0)

    class Meta:
        verbose_name = '账户信息表'
        db_table = 'account'


class RegionInfo(models.Model):
    firm_id = models.IntegerField(verbose_name='云厂商id')
    # 主机可用区：0     存储可用区： 1   阿里云只有一种

    region_type = models.IntegerField(verbose_name='地区类型', null=True)
    region_id = models.IntegerField(verbose_name='地区id')
    region_name = models.CharField(verbose_name='汉语名称', max_length=100)
    end_point = models.CharField(verbose_name='域名', max_length=200)

    # 0   不可用     1  可用
    region_status_choices = (
        (0, "不可用"),
        (1, "可用"),
    )
    region_status = models.IntegerField(verbose_name='可用状态', choices=region_status_choices, default=1)
    is_delete = models.IntegerField(verbose_name='是否删除', default=0)

    class Meta:
        verbose_name = '可用地区'
        db_table = 'region_info'


class HostInfo(models.Model):
    """
    服务器信息表
    """
    account_id = models.IntegerField(verbose_name='帐号id')
    instance_id = models.CharField(verbose_name='实例id', max_length=100)
    instance_name = models.CharField(verbose_name='实例名称', max_length=100)
    os_name = models.CharField(verbose_name='系统版本', max_length=100, null=True)
    # instance_des = models.CharField(verbose_name='实例描述', max_length=200)
    # 0-linux,1-windows,--其他依次添加
    # instance_network_type_choice = (
    #     ('classic', '经典网络'),
    #     ('vpc', 'VPC'),
    # )
    # instance_network_type = models.CharField(verbose_name='网络类型', max_length=50, choices=instance_network_type_choice)
    instance_type_choices = (
        (0, 'Linux'),
        (1, 'Windows'),
    )
    instance_type = models.IntegerField(verbose_name='系统类型', choices=instance_type_choices, null=True)
    instance_status_choices = (
        (0, '运行中'),
        (1, '启动中'),
        (2, '停止中'),
        (3, '已停止'),
    )

    instance_status = models.IntegerField(verbose_name='实例运行状态', choices=instance_status_choices, null=True)
    instance_pub_ip = models.CharField(verbose_name='公网ip', max_length=100, null=True)
    instance_pri_ip = models.CharField(verbose_name='内网ip', max_length=100, null=True)
    instance_vpc_ip = models.CharField(verbose_name='专有ip', max_length=100, null=True)
    network_interface_id = models.CharField(verbose_name='弹性网卡ip', max_length=100, null=True)
    internet_charge_type_choice = (
        (0, '按流量计费'),
        (1, '按带宽计费'),
    )
    internet_charge_type = models.IntegerField(verbose_name='网络计费方式', choices=internet_charge_type_choice, null=True)
    price_per_hour = models.CharField(verbose_name='每小时最高价', max_length=50, null=True)

    instance_charge_type_choice = (
        (0, '包年包月'),
        (1, '按量付费'),
    )
    instance_charge_type = models.IntegerField(verbose_name='实例计费方式', choices=instance_charge_type_choice, null=True)
    policy_id = models.IntegerField(verbose_name='策略id', null=True)
    region_id = models.IntegerField(verbose_name='地区id', null=True)
    start_time = models.DateTimeField(verbose_name='创建时间', default=datetime.datetime.now)
    end_time = models.DateTimeField(verbose_name='到期时间', default=datetime.datetime.now)
    last_buy_time = models.DateTimeField(verbose_name='上次续费时间', null=True)
    # 需要关联地区信息

    # lock_reason_choice = (
    #     ('financial', '因欠费被锁定'),
    #     ('security', '因安全原因被锁定'),
    #     ('recycling', '抢占式实例的待释放锁定状态'),
    #     ('dedicatedhostfinancial', '因为专有宿主机欠费导致 ECS 实例被锁定'),
    # )
    # lock_reason = models.CharField(verbose_name='锁定原因', max_length=100, null=True)

    is_overdue_choices = (
        (0, '使用中'),
        (1, '已过期'),
        (2, '锁定'),
    )
    is_overdue = models.IntegerField(verbose_name='使用状态', choices=is_overdue_choices, default=0)
    is_delete = models.IntegerField(verbose_name='是否删除', default=0)

    class Meta:
        verbose_name = '主机资源信息'
        db_table = 'host_info'


class StorageInfo(models.Model):
    account_id = models.IntegerField(verbose_name='账户ID')
    region_id = models.IntegerField(verbose_name='地区id', null=True)
    name = models.CharField(verbose_name='存储名', max_length=100)
    request_num = models.IntegerField(verbose_name='总请求次数')
    cdn = models.CharField(verbose_name='CDN回源流量', max_length=100, null=True)
    pub_net = models.CharField(verbose_name='外网访问流量', max_length=100, null=True)
    storage_size = models.CharField(verbose_name='存储使用量', max_length=1000)
    storage_type = models.CharField(verbose_name='存储类型', max_length=100, null=True)
    obj_num = models.CharField(verbose_name='文件数量 ', max_length=100, null=True)
    obj_list = models.TextField(verbose_name='文件列表', null=True)
    one_date = models.DateTimeField(verbose_name='每一天日期', null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', default=datetime.datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', default=datetime.datetime.now)
    is_delete = models.IntegerField(verbose_name='是否删除', default=0)

    class Meta:
        verbose_name = '云存储表'
        db_table = 'storage_info'


class BillInfo(models.Model):
    account_id = models.IntegerField(verbose_name='账户ID')

    # 实例 0     存储  1
    source_type = models.CharField(verbose_name='资源类型', max_length=100, null=True)
    source_id = models.CharField(verbose_name='资源id', max_length=200, null=True)
    source_name = models.CharField(verbose_name='资源名称', max_length=200, null=True)
    charge_type = models.CharField(verbose_name='计费类型', max_length=100, null=True)
    start_time = models.DateTimeField(verbose_name='开始日期', null=True)
    end_time = models.DateTimeField(verbose_name='结束日期', null=True)
    price = models.CharField(verbose_name='消费总金额', max_length=100, null=True)
    bandwidth_price = models.CharField(verbose_name='带宽消费', max_length=100, null=True)
    disk_price = models.CharField(verbose_name='磁盘消费', max_length=100, null=True)
    snapshot_price = models.CharField(verbose_name='快照消费', max_length=100, null=True)
    storage_type = models.CharField(verbose_name='存储类型', max_length=50, null=True)
    storage_flow_price = models.CharField(verbose_name='存储流量消费', max_length=100, null=True)
    storage_request_price = models.CharField(verbose_name='存储请求消费', max_length=100, null=True)
    storage_price = models.CharField(verbose_name='存储消费', max_length=100, null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', default=datetime.datetime.now)

    class Meta:
        verbose_name = '账单表'
        db_table = 'bill_info'


class DiskInfo(models.Model):
    account_id = models.IntegerField(verbose_name='账户ID')
    disk_id = models.IntegerField(verbose_name='磁盘id', null=True)
    policy_id = models.IntegerField(verbose_name='策略id', null=True)
    region_id = models.IntegerField(verbose_name='地区id', null=True)
    # disk_type:   0:系统盘    1:数据盘
    disk_type_choices = (
        (0, '系统盘'),
        (1, '数据盘')
    )
    disk_type = models.IntegerField(verbose_name='磁盘类型', choices=disk_type_choices, null=True)
    instance_id = models.IntegerField(verbose_name='对应的实例表id', null=True)
    disk_name = models.CharField(verbose_name='磁盘名', max_length=200, null=True)
    # 0.普通云盘   1.高效云盘    2.SSD云盘     3.本地SSD     4.本地磁盘
    disk_category_choices = (
        (0, '普通云盘'),
        (1, '高效云盘'),
        (2, 'SSD云盘'),
        (3, '本地SSD'),
        (4, '本地磁盘')
    )
    disk_category = models.IntegerField(verbose_name='磁盘类型', choices=disk_category_choices, default=0)
    encrypted = models.BooleanField(verbose_name='是否加密', default=False)
    disk_size = models.CharField(verbose_name='磁盘大小', max_length=500, null=True)
    # 0:使用中   1.可用     2.正在附加      3.正在拆卸   4.正在创建   5.重新初始化
    disk_status_choices = (
        (0, '使用中'),
        (1, '可用'),
        (2, '正在附加'),
        (3, '正在拆卸'),
        (4, '正在创建'),
        (5, '重新初始化')
    )
    disk_status = models.IntegerField(verbose_name='磁盘状态', choices=disk_status_choices, default=0, null=True)
    # 0: 包年包月    1.按量付费
    disk_charge_type_choices = (
        (0, '包年包月'),
        (1, '按量付费')
    )
    disk_charge_type = models.IntegerField(verbose_name='付费类型', choices=disk_charge_type_choices, default=0, null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', default=datetime.datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', default=datetime.datetime.now)
    # 0. 未删除   1.已删除
    is_delete = models.IntegerField(verbose_name='是否删除', default=0)

    class Meta:
        verbose_name = '磁盘表'
        db_table = 'disk_info'


class SnapshotPolicy(models.Model):
    account_id = models.IntegerField(verbose_name='账户id')
    region_id = models.IntegerField(verbose_name='地区id', null=True)
    policy_name = models.CharField(verbose_name='策略名称', max_length=100, null=True)
    # 0~23
    time_point = models.CharField(verbose_name='时间点', max_length=200, null=True)
    # 1~7
    week = models.CharField(verbose_name='快照重复日期', max_length=100, null=True)

    # -1   永久保存
    retention_days = models.IntegerField(verbose_name='自动快照保存天数', null=True)

    # -1   未知
    disk_num = models.IntegerField(verbose_name='启用该策略的磁盘数量', null=True)
    # 0 可用     1  创建中
    status_choices = (
        (0, "可用"),
        (1, "创建")
    )
    status = models.IntegerField(verbose_name='策略状态', choices=status_choices, default=0)

    policy_create_time = models.DateTimeField(verbose_name='策略创建时间', default=datetime.datetime.now)
    create_time = models.DateTimeField(verbose_name='创建时间', default=datetime.datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', default=datetime.datetime.now)
    is_delete = models.IntegerField(verbose_name='是否删除', default=0)

    class Meta:
        verbose_name = '快照策略表'
        db_table = 'snapshot_policy'


class SnapshotInfo(models.Model):
    account_id = models.IntegerField(verbose_name='账户id')
    region_id = models.IntegerField(verbose_name='地区id', null=True)
    instance_id = models.IntegerField(verbose_name='实例表id', null=True)
    disk_id = models.IntegerField(verbose_name='关联的磁盘', null=True)

    # 0. 可用  1.不可用
    available_status_choices = (
        (0, '可用'),
        (1, '不可用')
    )
    available_status = models.IntegerField(verbose_name='可用状态', choices=available_status_choices, default=0)
    snapshot_id = models.CharField(verbose_name='快照id', max_length=200, null=True)
    snapshot_name = models.CharField(verbose_name='快照名', max_length=200, null=True)
    # 0.自动创建的快照      1.手动创建的快照
    snapshot_type_choices = (
        (0, '自动创建'),
        (1, '手动创建')
    )
    snapshot_type = models.IntegerField(verbose_name='快照类型', choices=snapshot_type_choices, default=0)
    snapshot_progress = models.CharField(verbose_name='快照创建进度%', max_length=100, null=True)
    # 0. 未删除   1.已删除
    is_delete = models.IntegerField(verbose_name='是否删除', default=0)
    retention_days = models.IntegerField(verbose_name=u'自动快照保存天数', null=True)
    # 0.完成    1.进行中     2.失败
    snapshot_status_choices = (
        (0, '完成'),
        (1, '进行中'),
        (2, '失败')
    )
    snapshot_status = models.IntegerField(verbose_name='快照状态', default=0)
    source_disk_size = models.CharField(verbose_name='源磁盘容量G', max_length=100, null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', default=datetime.datetime.now)
    snapshot_create_time = models.DateTimeField(verbose_name='快照创建时间', default=datetime.datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', default=datetime.datetime.now)

    class Meta:
        verbose_name = '快照表'
        db_table = 'snapshot_info'


class PolicyHistory(models.Model):
    account_id = models.IntegerField(verbose_name='账户ID')
    policy_id = models.IntegerField(verbose_name='策略id', null=True)
    instance_id = models.IntegerField(verbose_name='对应的实例id', null=True)
    disk_id = models.IntegerField(verbose_name='关联的磁盘', null=True)
    # 0 成功    1 失败
    exec_status_choices = (
        (0, '成功'),
        (1, '失败'),
    )
    exec_status = models.IntegerField(verbose_name='执行状态', choices=exec_status_choices, default=0)
    # 0. 撤销    1.应用     2.删除
    operation_choices = (
        (0, '撤销'),
        (1, '应用'),
        (2, '删除'),
    )
    operation = models.IntegerField(verbose_name='执行的操作', choices=operation_choices, null=True)
    describe = models.CharField(verbose_name='信息描述', max_length=300, null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', default=datetime.datetime.now)
    is_delete = models.IntegerField(verbose_name='是否删除', default=0)

    class Meta:
        verbose_name = '策略历史记录表'
        db_table = 'policy_history'


class SnapshotHistory(models.Model):
    account_id = models.IntegerField(verbose_name='账户ID')
    snapshot_id = models.IntegerField(verbose_name='关联快照', null=True)
    disk_id = models.IntegerField(verbose_name='关联的磁盘', null=True)
    # 0 成功    1 失败
    exec_status_choices = (
        (0, '成功'),
        (1, '失败'),
    )
    exec_status = models.IntegerField(verbose_name='执行状态', choices=exec_status_choices, default=0)
    instance_id = models.IntegerField(verbose_name='关联的实例', null=True)
    # 0. 创建    1.回滚     2.删除
    operation_choices = (
        (0, '创建'),
        (1, '回滚'),
        (2, '删除'),
    )
    operation = models.IntegerField(verbose_name='执行的操作', choices=operation_choices, null=True)
    describe = models.CharField(verbose_name='信息描述', max_length=300, null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', default=datetime.datetime.now)
    is_delete = models.IntegerField(verbose_name='是否删除', default=0)

    class Meta:
        verbose_name = '快照历史记录表'
        db_table = 'snapshot_history'
