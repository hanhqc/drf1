from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect

# @csrf_protect
from rest_framework.views import APIView
from rest_framework.response import Response

from app1.models import User


@csrf_exempt
def user(request):
    if request.method == 'GET':  # 查询
        print(request.GET.get('name'))
        return HttpResponse('GET OK')

    if request.method == 'POST':  # 添加
        print(request.POST.get('name'))
        return HttpResponse('POST OK')

    if request.method == 'PUT':  # 修改
        print('PUT OK')
        return HttpResponse('PUT OK')

    if request.method == 'DELETE':  # 删除
        print('DELETE OK')
        return HttpResponse('DELETE OK')

    if request.method == 'PATCH':  # 局部修改
        print('PATCH OK')
        return HttpResponse('PATCH OK')


@method_decorator(csrf_exempt, name='dispatch')
class UserView(View):

    def get(self, request, *args, **kwargs):
        print('GET OK')
        return HttpResponse('GET OK')

    def post(self, request, *args, **kwargs):
        print('POST OK')
        return HttpResponse('POST OK')

    def put(self, request, *args, **kwargs):
        print('PUT OK')
        return HttpResponse('PUT OK')

    def delete(self, request, *args, **kwargs):
        print('DELETE OK')
        return HttpResponse('DELETE OK')

    def patch(self, request, *args, **kwargs):
        print('PATCH OK')
        return HttpResponse('PATCH OK')


@method_decorator(csrf_exempt, name='dispatch')
class Employee(View):

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if id:
            user_obj = User.objects.filter(id=id).values().first()
            if user_obj:
                return JsonResponse({
                    'status': 200,
                    'msg': '查询单个用户成功',
                    'result': user_obj
                })
        else:
            user_list = User.objects.all().values()
            return JsonResponse({
                'status': 200,
                'msg': '查询所有用户成功',
                'result': list(user_list)
            })

        return JsonResponse({
            'status': 500,
            'msg': '查询用户不存在'
        })

    def post(self, request, *args, **kwargs):

        name = request.POST.get('name')
        pwd = request.POST.get('pwd')

        try:
            user_obj = User.objects.create(name=name, pwd=pwd)
            return JsonResponse({
                'status': 200,
                'msg': '创建用户成功',
                'result': {'name': user_obj.name}
            })
        except:
            return JsonResponse({
                'status': 500,
                'msg': '创建新用户失败'
            })


class Student(APIView):

    # 查询  单个  全部
    def get(self, request, *args, **kwargs):

        id = kwargs.get('id')
        if id:
            user_obj = User.objects.filter(id=id).values().first()
            if user_obj:
                return Response({
                    'status': 200,
                    'msg': '查询单个用户成功',
                    'result': user_obj
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

    # 添加用户
    def post(self, request, *args, **kwargs):

        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        try:
            user_obj = User.objects.create(name=name, pwd=pwd)
            return Response({
                'status': 200,
                'msg': '创建用户成功',
                'result': {'name': user_obj.name}
            })
        except:
            return Response({
                'status': 500,
                'msg': '创建用户失败',
            })

    # 删除用户
    def delete(self, request, *args, **kwargs):
        name = request.GET.get('name')
        user_obj = User.objects.filter(name=name)
        if user_obj:
            try:
                with transaction.atomic():
                    user_obj.delete()
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

    # 修改用户数据
    def put(self, request, *args, **kwargs):
        id = request.GET.get('id')
        pwd = request.GET.get('pwd')
        user_obj = User.objects.get(id=id)
        if user_obj:
            try:
                with transaction.atomic():
                    user_obj.pwd = pwd
                    user_obj.save()
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