from django.views import View
from django import http
import json
from api.models import UserInfo, UserDetailInfo, RecordsInfo, KeyInfo
from rest_framework import viewsets
from rest_framework import generics
from . import models
from . import serializers
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView


# ---------------------------用户类(初始注册账号)---------------------------------
# 列表视图
class UserInfoView(APIView):
    # 查询所有用户的用户名和密码
    def get(self, request):
        # 1.查询所有用户信息
        users = UserInfo.objects.all()

        # 2.数据转换
        user_list = []
        for user in users:
            user_dict = {
                "id": user.id,
                "username": user.username,
                "password": user.password,
                "certification": user.certification
            }
            user_list.append(user_dict)

        # 3.返回响应
        return http.JsonResponse(user_list, safe=False)

    # 创建一个用户
    def post(self, request):
        # 1.获取参数
        dict_data = json.loads(request.body.decode())
        username = dict_data.get("username")
        password = dict_data.get("password")
        # 2.校验参数
        # 3.数据入库
        user = UserInfo.objects.create(**dict_data)
        # 4.返回响应, 响应值201
        user_dict = {
            "id": user.id,
            "username": user.username,
            "password": user.password,
        }
        return http.JsonResponse(user_dict, status=201)


# 详细视图
class UserInfoDetailView(APIView):
    # 查询某个用户的用户名和密码以及认证情况
    def get(self, request, pk):
        # 1.通过pk获取对象
        user = UserInfo.objects.get(pk=pk)
        # 2.转换数据
        user_dict = {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "certification": user.certification,
        }
        # 3.返回响应
        return http.JsonResponse(user_dict)

    # 修改某个用户的用户名和密码以及认证情况
    def put(self, request, pk):
        # 1.通过pk获取对象
        user = UserInfo.objects.get(pk=pk)
        # 2.获取参数
        dict_data = json.loads(request.body.decode())
        # 3.校验参数
        # 4.数据入库
        UserInfo.objects.filter(pk=pk).update(**dict_data)
        user = UserInfo.objects.get(pk=pk)
        user_dict = {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "certification": user.certification,
        }
        # 5.返回响应
        return http.JsonResponse(user_dict)

    # 删除某个用户
    def delete(self, request, pk):
        # 1.通过参数获取用户
        user = UserInfo.objects.get(id=pk)
        # 2.删除用户
        user.delete()
        # 3.返回204
        return http.HttpResponse(status=204)


# ---------------------------用户详细信息类(身份认证)------------------------------
# 详细视图
class UserDetailInfoView(APIView):
    # 获取用户详细信息
    def get(self, request, pk):
        # 1.通过pk获取对象
        user = UserInfo.objects.get(pk=pk)
        detail = UserDetailInfo.objects.get(user_id=user.id)
        # 2.转换数据
        user_dict = {
            "id": user.id,
            "username": user.username,
            "phone": detail.phone,
            "group": detail.group,
            "job": detail.job,
            "email": detail.email,
        }
        # 3.返回响应
        return http.JsonResponse(user_dict)

    # 创建用户详细信息
    def post(self, request, pk):
        # 1.获取参数
        dict_data = json.loads(request.body.decode())
        user = UserInfo.objects.get(pk=pk)
        user.certification = True
        phone = dict_data.get("phone")
        group = dict_data.get("group")
        job = dict_data.get("job")
        email = dict_data.get("email")
        detail_dict = {
            "user_id": user.id,
            "phone": phone,
            "group": group,
            "job": job,
            "email": email,
        }
        # print(detail_dict)
        # 2.校验参数
        # 3.数据入库
        user = UserDetailInfo.objects.create(**detail_dict)
        # 4.返回响应, 响应值201
        return http.JsonResponse(detail_dict, status=201)

    # 更新用户详细信息
    def put(self, request, pk):
        # 1.通过pk获取对象
        user = UserInfo.objects.get(pk=pk)
        # 2.获取参数
        dict_data = json.loads(request.body.decode())
        # 3.校验参数
        # 4.数据入库
        UserDetailInfo.objects.filter(pk=pk).update(**dict_data)
        detail = UserDetailInfo.objects.get(user_id=user.id)
        user_dict = {
            "username": user.username,
            "user_id": user.id,
            "phone": detail.phone,
            "group": detail.group,
            "job": detail.job,
            "email": detail.email,
        }
        # 5.返回响应
        return http.JsonResponse(user_dict)


# ---------------------------预约记录类(全部预约记录查询)---------------------------
# 列表视图
class RecordInfoView(APIView):
    # 查询整个系统里的所有预约记录
    def get(self, request):
        # 1.查询所有预约记录
        records = RecordsInfo.objects.all()

        # 2.数据转换
        record_list = []
        for record in records:
            user = UserInfo.objects.get(id=record.user_id)
            detail = UserDetailInfo.objects.get(user_id=user.id)
            record_dict = {
                "user_id": user.id,
                "username": user.username,
                "group": detail.group,
                "starttime": record.starttime,
                "endtime": record.endtime,
                "choice": record.choice,
                "text": record.text,
            }
            record_list.append(record_dict)

        # 3.返回响应
        return http.JsonResponse(record_list, safe=False)


# ---------------------------预约记录类(个人预约记录操作)---------------------------
# 详细视图
class UserRecordInfoView(APIView):
    # 查询某个用户的所有预约记录
    def get(self, request, pk):
        # 1.查询个人预约记录
        user = UserInfo.objects.get(pk=pk)
        records = RecordsInfo.objects.filter(user_id=user.id)
        detail = UserDetailInfo.objects.get(user_id=user.id)
        # 2.数据转换
        record_list = []
        for record in records:
            record_dict = {
                "user_id": user.id,
                "username": user.username,
                "group": detail.group,
                "starttime": record.starttime,
                "endtime": record.endtime,
                "choice": record.choice,
                "text": record.text,
            }
            record_list.append(record_dict)

        # 3.返回响应
        return http.JsonResponse(record_list, safe=False)

    # 创建一条预约记录
    def post(self, request, pk):
        # 1.获取参数
        dict_data = json.loads(request.body.decode())
        user_id = dict_data.get("user_id")
        user = UserInfo.objects.get(id=user_id)
        starttime = dict_data.get("starttime")
        endtime = dict_data.get("endtime")
        choice = dict_data.get("choice")
        text = dict_data.get("text")
        detail_dict = {
            "user_id": user_id,
            "starttime": starttime,
            "endtime": endtime,
            "choice": choice,
            "text": text,
        }
        # print(detail_dict)
        # 2.校验参数
        # 3.数据入库
        record = RecordsInfo.objects.create(**detail_dict)
        detail = UserDetailInfo.objects.get(user_id=user_id)
        # 4.返回响应, 响应值201
        res = {
            "pk": record.pk,
            "user_id": user_id,
            "username": user.username,
            "group": detail.group,
            "starttime": starttime,
            "endtime": endtime,
            "choice": choice,
            "text": text,
        }
        return http.JsonResponse(res, status=201)


class UserRecordInfoDetailView(APIView):
    # 查询某一条特定的预约记录 通过用户pk和预约记录pk两个参数传入
    def get(self, request, pk1, pk2):
        # 1.查询个人预约记录
        user = UserInfo.objects.get(pk=pk1)
        record = RecordsInfo.objects.get(pk=pk2)
        detail = UserDetailInfo.objects.get(user_id=user.id)
        # 2.数据转换
        record_dict = {
            "user_id": user.id,
            "username": user.username,
            "group": detail.group,
            "starttime": record.starttime,
            "endtime": record.endtime,
            "choice": record.choice,
            "text": record.text,
        }
        # 3.返回响应
        return http.JsonResponse(record_dict)

    # 修改某一条特定的预约记录 通过用户pk和预约记录pk两个参数传入
    def put(self, request, pk1, pk2):
        # 1.通过pk获取对象
        user = UserInfo.objects.get(pk=pk1)
        record = RecordsInfo.objects.get(pk=pk2)
        detail = UserDetailInfo.objects.get(user_id=user.id)
        # 2.获取参数
        dict_data = json.loads(request.body.decode())
        # 3.校验参数
        # 4.数据入库
        RecordsInfo.objects.filter(pk=pk2).update(**dict_data)
        record = RecordsInfo.objects.get(pk=pk2)
        record_dict = {
            "username": user.username,
            "user_id": user.id,
            "group": detail.group,
            "starttime": record.starttime,
            "endtime": record.endtime,
            "choice": record.choice,
            "text": record.text,
        }
        # 5.返回响应
        return http.JsonResponse(record_dict)

    # 删除某一条特定的预约记录 通过用户pk和预约记录pk两个参数传入
    def delete(self, request, pk1, pk2):
        # 1.通过参数获取用户
        record = RecordsInfo.objects.get(pk=pk2)
        # 2.删除用户
        record.delete()
        # 3.返回204
        return http.HttpResponse(status=204)


# -----------------------------------钥匙视图------------------------------------
class KeyInfoView(APIView):
    # 获取钥匙位置
    def get(self, request):
        where_is_key = KeyInfo.objects.get(pk=1)
        key_dict = {
            "whereiskey": where_is_key.where_is_key,
        }
        return http.JsonResponse(key_dict)

    # 更新钥匙位置
    def put(self, request):
        dict_data = json.loads(request.body.decode())
        where_is_key = dict_data.get("whereiskey")
        detail_dict = {
            "where_is_key": where_is_key,
        }
        KeyInfo.objects.filter(pk=1).update(**detail_dict)
        res = {
            "whereiskey": where_is_key,
        }
        return http.JsonResponse(res, status=201)
