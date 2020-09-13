from django.db import transaction
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from app1.models import User


class Student(APIView):
    # 查询单个 查询所有
    def get(self, request):
        id = request.query_params.get('id')
        # print(id, type(id))
        if id:
            user = User.objects.filter(pk=id).values().first()
            if user:
                return Response({
                    'status': 200,
                    'msg': '查询单个用户成功',
                    'result': user
                })
        else:
            user_list = User.objects.all().values()
            return Response({
                'status': 200,
                'msg': '查询全部用户成功',
                'result': list(user_list)
            })
        return Response({
            "status": 500,
            "msg": "查询用户不存在",
        })

    # 新增单个
    def post(self, request):
        name = request.data.get('name')
        pwd = request.data.get('pwd')
        # print(name, pwd)
        try:
            with transaction.atomic():
                user = User.objects.create(name=name, pwd=pwd)
                return Response({
                    'status': 200,
                    'msg': '创建用户成功',
                    'result': {'id': user.id, 'name': user.name}
                })
        except:
            return Response({
                'status': 500,
                'msg': '创建用户失败',
            })

    # 修改
    def put(self, request):
        id = request.query_params.get('id')
        pwd = request.query_params.get('pwd')
        user = User.objects.get(id=id)
        if user:
            try:
                with transaction.atomic():
                    user.pwd = pwd
                    user.save()
                    return Response({
                        "status": 200,
                        "msg": '密码修改成功',
                    })
            except:
                return Response({
                    "status": 500,
                    "msg": '密码修改失败',
                })
        return Response({
            "status": 500,
            "msg": f'无id为  {id}  的用户',
        })

    # 删除
    def delete(self, request):
        name = request.query_params.get('name')
        user = User.objects.filter(name=name)
        if user:
            try:
                with transaction.atomic():
                    user.delete()
                    return Response({
                        "status": 200,
                        "msg": f'删除用户  {name}  成功',
                    })
            except:
                return Response({
                    "status": 500,
                    "msg": f'删除用户  {name}  失败',
                })

        return Response({
            "status": 500,
            "msg": f"用户  {name}  不存在",
        })
