from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from myauth import auth
from public_cloud import ResponseData
from public_cloud import models
from public_cloud import serializers


class CreateFamily(APIView):
    """
    家族类
    """
    authentication_classes = [auth.MyAuthentication]

    def dispatch(self, request, *args, **kwargs):
        return super(CreateFamily, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = ResponseData.ResponseData().response_data()
        user_id = request.data.get('user_id', '')
        family_name = request.data.get('family_name', '')
        if user_id and family_name:
            family = models.Family.objects.create(user_id=user_id, family_name=family_name)
            serializer = serializers.FamilySerializer(family)
            response['data']['obj'] = serializer.data
        else:
            response['code'] = 1
            response['msg'] = '参数错误'

        return Response(response, status=status.HTTP_200_OK)


class GetFamily(APIView):
    """
    家族类
    """
    authentication_classes = [auth.MyAuthentication]

    def dispatch(self, request, *args, **kwargs):
        return super(GetFamily, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = ResponseData.ResponseData().response_data()
        user_id = request.data.get('user_id', '')
        if user_id:
            families = models.Family.objects.filter(user_id=user_id, is_delete=0)
            serializer = serializers.FamilySerializer(families, many=True)
            response['data']['obj'] = serializer.data
        else:
            response['code'] = 1
            response['msg'] = '用户为空'

        return Response(response, status=status.HTTP_200_OK)


class AddAccount(APIView):
    """
    录入账户
    """
    authentication_classes = [auth.MyAuthentication]

    def dispatch(self, request, *args, **kwargs):
        return super(AddAccount, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = {
            'code': 0,
            'msg': 'success',
            'data': {}
        }
        access_key = request.data.get('access_key', '')
        secret_key = request.data.get('secret_key', '')
        app_id = request.data.get('app_id', '')
        family_id = request.data.get('family_id', '')
        firm_key = request.data.get('firm_key', '')
        if (access_key and secret_key and firm_key and family_id):
            models.AccountInfo.objects.update_or_create(access_key=access_key,
                                                        is_delete=0,
                                                        defaults={
                                                            'access_key': access_key,
                                                            'firm_key': firm_key,
                                                            'secret_key': secret_key,
                                                            'app_id': app_id,
                                                            'family_id': family_id
                                                        })
        else:
            response['code'] = 1
            response['msg'] = '参数错误'

        return Response(response, status=status.HTTP_200_OK)


class GetAccount(APIView):
    """
    获取账户详情
    """
    authentication_classes = [auth.MyAuthentication]

    def dispatch(self, request, *args, **kwargs):
        return super(GetAccount, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = ResponseData.ResponseData().response_data()
        user_id = request.data.get('user_id', '')
        # ali = aliyun.AliyunOperator(access_key='LTAIkLqvvsa0zXcZ', secret_key='TQ7LLCxyPwVEwSSvSKzO5PdN4j2lfZ')
        # ali.api_get_region_info_to_model()
        families = models.Family.objects.filter(user_id=user_id, is_delete=0)
        data = []

        for family in families:
            one_data = {}
            one_data['family_name'] = family.family_name
            one_data['family_id'] = family.id
            one_data['create_time'] = family.create_time
            one_data['all_account_count'] = models.AccountInfo.objects.filter(family_id=family.id, is_delete=0).count()
            data.append(one_data)

        response['data']['obj'] = data

        return Response(response, status=status.HTTP_200_OK)


class GetFirm(APIView):
    """
    获取云厂商
    """
    authentication_classes = [auth.MyAuthentication]

    def dispatch(self, request, *args, **kwargs):
        return super(GetFirm, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = ResponseData.ResponseData().response_data()
        firms = models.FirmInfo.objects.filter()
        serializer = serializers.FirmSerializer(firms, many=True)
        response['data']['obj'] = serializer.data
        return Response(response, status=status.HTTP_200_OK)


class GetFamilyFirm(APIView):
    """
    获取该Family拥有的云厂商
    """

    def dispatch(self, request, *args, **kwargs):
        return super(GetFamilyFirm, self).dispatch(request, *args, **kwargs)

    pass
