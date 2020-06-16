import traceback

from django.http.response import HttpResponse
from rest_framework.views import APIView

from cloud.fs.conf.dialplan import Dialplan


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
                    response = handle.respond(404)
                else:
                    xml = handle.generate_public_xml(mobile)
                    response = handle.to_xml(xml)
        except Exception as e:
            print(request.data, e)
            traceback.print_exc()
            handle.respond(500)
        return HttpResponse(response, content_type='text/xml')

    def get_real_number(self, dest):
        '''获取真实号码
        '''
        return dest
