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


class AccountView(APIView):
    """
    录入账户
    """

    def dispatch(self, request, *args, **kwargs):
        return super(AccountView, self).dispatch(request, *args, **kwargs)

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
        firm_id = request.data.get('firm_id', '')
        if (access_key and secret_key and firm_id and family_id):
            models.AccountInfo.objects.update_or_create(access_key=access_key, defaults={
                access_key: access_key,
                firm_id: firm_id,
                secret_key: secret_key,
                app_id: app_id,
                family_id: family_id
            })
        else:
            response['code'] = 1
            response['msg'] = '值错误'

        return Response(response, status=status.HTTP_200_OK)
