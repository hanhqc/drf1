from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework.views import status


def exception_handler(exc, context):
    # 格式化异常信息
    error = "%s %s %s" % (context['view'], context['request'].method, exc)
    print(error)
    # 1.先用drf自己处理异常的方法进行处理
    response = drf_exception_handler(exc, context)
    # 2.用drf自身处理异常忽悠一个返回值 如果返回值为空，表示drf自身无法解决异常，则需要我们自定义方法去解决
    if response is None:
        return Response(
            {"msg": "异常处理中~"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=None)
    # 3.如果drf自身吃力异常的方法的返回值不为空 说明异常被drf自身解决
    return response
