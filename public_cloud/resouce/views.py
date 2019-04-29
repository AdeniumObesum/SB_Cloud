import traceback
import time
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from myauth import auth
from public_cloud import ResponseData
from public_cloud import models
from public_cloud import serializers
from public_cloud.cloud_api.CloudDic import CloudDic


class ImportHost(APIView):
    """
    导入云主机
    """
    authentication_classes = [auth.MyAuthentication]

    def dispatch(self, request, *args, **kwargs):
        return super(ImportHost, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = ResponseData.ResponseData(code=0, msg='success', data= {}).response_data()
        account_id = request.data.get('account_id', '')
        firm_key = request.data.get('firm_key', '')
        account = models.AccountInfo.objects.get(id=account_id)
        try:
            CloudDic[firm_key](access_key=account.access_key, secret_key=account.secret_key).api_get_ecs_to_model()
            account.is_import = 1
            account.save()
            response['msg'] = '已导入，请到资源管理页面查看主机'
        except Exception as e:
            traceback.print_exc()
            response['code'] = 1
            response['msg'] = '导入主机失败，请检查密匙是否可用'
        return Response(response, status=status.HTTP_200_OK)


class GetFamilyFirm(APIView):
    """
    获取该Family拥有的云厂商
    """
    authentication_classes = [auth.MyAuthentication]

    def dispatch(self, request, *args, **kwargs):
        return super(GetFamilyFirm, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = ResponseData.ResponseData(code=0, msg='success', data={}).response_data()
        family_id = request.data.get('family_id', '')
        dic = {}
        data = []
        accounts = models.AccountInfo.objects.filter(family_id=family_id, is_delete=0)
        for account in accounts:
            dic[account.firm_key] = models.FirmInfo.objects.get(firm_key=account.firm_key).zh_name

        for key, value in dic.items():
            new_dic = {}
            new_dic['firm_key'] = key
            new_dic['firm_name'] = value
            data.append(new_dic)
        response['data']['obj'] = data
        return Response(response, status=status.HTTP_200_OK)

    pass


class GetHost(APIView):
    """获取主机"""

    authentication_classes = [auth.MyAuthentication]

    def dispatch(self, request, *args, **kwargs):
        return super(GetHost, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = ResponseData.ResponseData(code=0, msg='success', data={}).response_data()
        family_id = request.data.get('family_id', '')
        firm_key = request.data.get('firm_key', '')
        accounts = models.AccountInfo.objects.filter(family_id=family_id, firm_key=firm_key, is_delete=0)
        data = []
        for account in accounts:
            hosts = models.HostInfo.objects.filter(account_id=account.id, is_delete=0, is_import=1)
            serializer = serializers.HostInfoSerializer(hosts, many=True)
            data += serializer.data
        response['data']['obj'] = data

        return Response(response, status=status.HTTP_200_OK)


class StopInstance(APIView):
    """
    关闭实例
    """
    authentication_classes = [auth.MyAuthentication]

    def dispatch(self, request, *args, **kwargs):
        return super(StopInstance, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = ResponseData.ResponseData(code=0, msg='success', data={}).response_data()
        firm_key = request.data.get('firm_key', '')
        instance_id = request.data.get('instance_id', '')
        account_id = request.data.get('account_id', '')
        account = models.AccountInfo.objects.get(id=account_id)
        try:
            data = CloudDic[firm_key](access_key=account.access_key, secret_key=account.secret_key).api_stop_instance(
                instance_id=instance_id)
            response['code'] = data['code']
            response['msg'] = data['msg']
            if data['code'] == 0:
                models.HostInfo.objects.filter(instance_id=instance_id).update(instance_status=3)  # #  其实有很多其他状态，暂时这么处理
        except Exception as e:
            traceback.print_exc()
            response['code'] = 1
            response['msg'] = '关机异常'
        return Response(response, status=status.HTTP_200_OK)


class StartInstance(APIView):
    """
    关闭实例
    """
    authentication_classes = [auth.MyAuthentication]

    def dispatch(self, request, *args, **kwargs):
        return super(StartInstance, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = ResponseData.ResponseData(code=0, msg='success', data={}).response_data()
        firm_key = request.data.get('firm_key', '')
        instance_id = request.data.get('instance_id', '')
        account_id = request.data.get('account_id', '')
        account = models.AccountInfo.objects.get(id=account_id)
        try:
            data = CloudDic[firm_key](access_key=account.access_key, secret_key=account.secret_key).api_start_instance(
                instance_id=instance_id)
            response['code'] = data['code']
            response['msg'] = data['msg']
            if data['code'] == 0:
                models.HostInfo.objects.filter(instance_id=instance_id).update(instance_status=0)  # #  其实有很多其他状态，暂时这么处理
        except Exception as e:
            traceback.print_exc()
            response['code'] = 0
            response['msg'] = '开机异常'
        return Response(response, status=status.HTTP_200_OK)


class GetDisk(APIView):
    """
    获取磁盘信息
    """
    authentication_classes = [auth.MyAuthentication]

    def dispatch(self, request, *args, **kwargs):
        return super(GetDisk, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = ResponseData.ResponseData(code=0, msg='success', data={}).response_data()
        firm_key = request.data.get('firm_key', '')
        # instance_id = request.data.get('instance_id', '')
        # account_id = request.data.get('account_id', '')
        family_id = request.data.get('family_id', '')

        accounts = models.AccountInfo.objects.filter(firm_key=firm_key, family_id=family_id, is_delete=0)
        data = []
        for account in accounts:
            disks = models.DiskInfo.objects.filter(account_id=account.id, is_cancel=0, is_delete=0)
            for disk in disks:
                dic = {}
                instance = models.HostInfo.objects.get(id=disk.instance_id)
                snapshots = models.SnapshotInfo.objects.filter(disk_id=disk.id, is_delete=0).order_by(
                    '-snapshot_create_time')

                dic['instance_type_id'] = instance.instance_type
                dic['instance_name'] = instance.instance_name
                dic['pub_ip'] = instance.instance_pub_ip
                dic['pri_ip'] = instance.instance_pri_ip
                dic['disk_id'] = disk.id
                dic['region_id'] = disk.region_id
                dic['disk_name'] = disk.disk_name
                dic['disk_size'] = disk.disk_size
                dic['disk_type'] = disk.get_disk_type_display()
                dic['snapshot_count'] = snapshots.count()
                dic['disk_long_id'] = disk.disk_id
                dic['account_id'] = disk.account_id
                dic['last_create_time'] = snapshots[0].snapshot_create_time.strftime('%Y-%m-%d')
                data.append(dic)

        response['data']['obj'] = data
        return Response(response, status=status.HTTP_200_OK)


class GetSnapshot(APIView):
    """
    获取快照信息
    """
    authentication_classes = [auth.MyAuthentication]

    def dispatch(self, request, *args, **kwargs):
        return super(GetSnapshot, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = ResponseData.ResponseData(code=0, msg='success', data={}).response_data()
        firm_key = request.data.get('firm_key', '')
        # instance_id = request.data.get('instance_id', '')
        # account_id = request.data.get('account_id', '')
        family_id = request.data.get('family_id', '')

        accounts = models.AccountInfo.objects.filter(firm_key=firm_key, family_id=family_id, is_delete=0)
        data = []
        for account in accounts:
            disks = models.DiskInfo.objects.filter(account_id=account.id, is_cancel=0)
            for disk in disks:
                instance = models.HostInfo.objects.get(id=disk.instance_id)
                snapshots = models.SnapshotInfo.objects.filter(disk_id=disk.id, is_delete=0).order_by(
                    'snapshot_create_time')
                for snapshot in snapshots:
                    dic = {}
                    dic['instance_type_id'] = instance.instance_type
                    dic['instance_name'] = instance.instance_name
                    dic['pub_ip'] = instance.instance_pub_ip
                    dic['pri_ip'] = instance.instance_pri_ip
                    dic['disk_id'] = disk.id
                    dic['region_id'] = disk.region_id
                    dic['disk_name'] = disk.disk_name
                    dic['snapshot_name'] = snapshot.snapshot_name
                    dic['source_disk_size'] = snapshot.source_disk_size
                    dic['account_id'] = snapshot.account_id
                    dic['snapshot_id'] = snapshot.snapshot_id
                    dic['snapshot_create_time'] = snapshot.snapshot_create_time.strftime('%Y-%m-%d')

                    data.append(dic)

        response['data']['obj'] = data
        return Response(response, status=status.HTTP_200_OK)


class DeleteSnapshot(APIView):
    """
    删除快照信息
    """
    authentication_classes = [auth.MyAuthentication]

    def dispatch(self, request, *args, **kwargs):
        return super(DeleteSnapshot, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        response = ResponseData.ResponseData(code=0, msg='success', data={}).response_data()
        firm_key = request.data.get('firm_key', '')
        snapshot_id = request.data.get('snapshot_id', '') # String ID
        account_id = request.data.get('account_id', '')
        try:
            account = models.AccountInfo.objects.filter(id=account_id, is_delete=0).first()
            rest = CloudDic[firm_key](access_key=account.access_key, secret_key=account.secret_key).api_delete_snapshot(snapshot_id=snapshot_id)
            if rest['code'] == 0:
                models.SnapshotInfo.objects.filter(is_delete=0, account_id=account_id, snapshot_id=snapshot_id).update(is_delete=1)
                response['msg'] = '已删除'
            else:
                response['code'] = 1
                response['msg'] = '删除失败，权限不足'
        except Exception as e:
            traceback.print_exc()
            response['code'] = 1
            response['msg'] = '系统异常'
        return Response(response, status=status.HTTP_200_OK)


class CreateSnapshot(APIView):
    """创建快照"""

    authentication_classes = [auth.MyAuthentication]

    def dispatch(self, request, *args, **kwargs):
        return super(CreateSnapshot, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = ResponseData.ResponseData(code=0, msg='success', data={}).response_data()
        account_id = request.data.get('account_id', '')
        firm_key = request.data.get('firm_key', '')
        disk_id = request.data.get('disk_id', '')
        name = request.data.get('name', '')
        description = request.data.get('description', '')
        account = models.AccountInfo.objects.get(id=account_id)
        try:
            if not name:
                name = '云平台管理_' + str(time.time())
            data = CloudDic[firm_key](access_key=account.access_key, secret_key=account.secret_key).api_create_snapshot(
                snapshot_name=name,
                disk_id=disk_id,
                description=description
            )
            response['code'] = data['code']
            response['msg'] = data['msg']
        except Exception as e:
            traceback.print_exc()
            response['code'] = 1
            response['msg'] = '系统异常'

        return Response(response, status=status.HTTP_200_OK)

# 回滚快照
class RollbackSnapshot(APIView):
    """回滚快照"""

    authentication_classes = [auth.MyAuthentication]

    def dispatch(self, request, *args, **kwargs):
        return super(RollbackSnapshot, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = ResponseData.ResponseData(code=0, msg='success', data={}).response_data()
        account_id = request.data.get('account_id', '')
        firm_key = request.data.get('firm_key', '')
        disk_id = request.data.get('disk_id', '')
        snapshot_id = request.data.get('snapshot_id', '')
        return Response(response, status=status.HTTP_200_OK)

class CancelInstance(APIView):
    """
    取消管理
    """
    authentication_classes = [auth.MyAuthentication]

    def dispatch(self, request, *args, **kwargs):
        return super(CancelInstance, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = ResponseData.ResponseData(code=0, msg='success', data= {}).response_data()
        instance_id = request.data.get('instance_id', '')
        try:
            instance = models.HostInfo.objects.filter(instance_id=instance_id)
            instance.update(is_import=0)
            models.DiskInfo.objects.filter(instance_id=instance[0].id).update(is_cancel=1)
            response['code'] = 0
            response['msg'] = '执行成功'
        except Exception as e:
            traceback.print_exc()
            response['code'] = 1
            response['msg'] = '撤销失败'
        return Response(response, status=status.HTTP_200_OK)


