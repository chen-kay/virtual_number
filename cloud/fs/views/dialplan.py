import traceback

from django.http.response import HttpResponse
from rest_framework import exceptions
from rest_framework.views import APIView

from cloud.fs.conf.dialplan import Dialplan
from cloud.fs.handle import get_call_mobile
from django_redis import get_redis_connection


class MobileNotFound(Exception):
    """
    号码不存在
    """


class MobileBlack(Exception):
    """
    号码黑名单
    """


class DialplanViews(APIView):
    '''拨号路由
    '''
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        handle = Dialplan(request.data)
        try:
            if handle.check_virtual_number():
                mobile = self.get_real_number(handle.dest)
                if not mobile:
                    xml = handle.respond(404)
                else:
                    xml = handle.generate_public_xml(mobile)
        except MobileNotFound:
            xml = handle.respond(404)
        except MobileBlack:
            xml = handle.respond(606)
        except Exception as e:
            print(request.data, e)
            traceback.print_exc()
            xml = handle.respond(500)
        return HttpResponse(handle.to_xml(xml), content_type='text/xml')

    def get_real_number(self, dest):
        '''获取真实号码
        '''
        mobile = get_call_mobile(dest)
        if not mobile:
            mobile = dest
            # raise MobileNotFound()
        if self.check_black_mobile(mobile):
            raise MobileBlack()
        return mobile

    def check_black_mobile(self, mobile):
        conn = get_redis_connection()
        return conn.sismember('blackphone', mobile)
