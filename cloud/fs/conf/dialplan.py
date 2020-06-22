from cloud.fs.handle import get_call_mobile
from cloud.fs.settings import fs_settings
from cloud.fs.utils import encry_sign
from freeswitch import XMLCurlFactory
from freeswitch.dialplan.condition import Condition
from freeswitch.dialplan.context import Context


class Dialplan:
    xml = None
    section = 'dialplan'

    def __init__(self, data):
        self.context = data.get('Caller-Context')
        self.dest = data.get('Caller-Destination-Number', None)

    def check_virtual_number(self):
        '''判断是否需要路由
        '''
        if self.context != 'public':
            return False
        return True

    def generate_public_xml(self, dest):
        mobile = get_call_mobile(dest)
        if not mobile:
            # 未找到
            return self.respond(404)

        data = [('sys_bridge', False,
                 [('destination_number', '^(.*)$', False, [
                     ('bridge', 'sofia/external/{0}@{1}'.format(
                         mobile, fs_settings.DEFAULT_GATEWAY_REAML), False),
                 ])])]
        xml = Context(self.context)
        self._generate_xml(xml, data)
        return xml

    def _generate_xml(self, context, data):
        for extension, continue_, conds in data:
            ext = context.addExtension(extension, continue_)
            for field, exp, cont, acts in conds:
                cond = Condition(attr=field, val=exp)
                for act, val, inline in acts:
                    cond.addAction(act, val)
                ext.addCondition(cond)

    def to_xml(self, data):
        xml = XMLCurlFactory(data=data.todict() if data else None,
                             section=self.section)
        return xml.convert()

    def respond(self, status):
        data = [
            ('sys_respond', False, [('destination_number', '^(.*)$', False, [
                ('respond', str(status), False),
            ])]),
        ]
        xml = Context(self.context)
        self._generate_xml(xml, data)
        return xml

    def request_mobile(self):
        '''请求mobile
        '''
