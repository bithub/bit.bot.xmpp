import json

from zope.interface import implements
from zope.component import getUtility

from twisted.python import log

from bit.core.interfaces import IConfiguration
from bit.bot.common.interfaces import IIntelligent, ISocketRequest


class XMPPMessageRequest(object):
    implements(ISocketRequest)

    def __init__(self, proto):
        self.proto = proto

    def response(self, msg):
        log.msg('bit.bot.http.request: MessageRequest.response: ', msg)
        self.proto.transport.write(json.dumps(msg))

    def load(self, sessionid, msg):
        log.msg('bit.bot.http.request: MessageRequest.load: ',
                sessionid, msg)
        self.session_id = sessionid
        domain = getUtility(IConfiguration).get('bot', 'domain')
        if domain == sessionid.split('/')[0].split('@')[1]:
            getUtility(
                IIntelligent).bot.setPredicate('secure', 'yes', sessionid)
        ask = getUtility(IIntelligent).respond(self, msg, sessionid)
        ask.addCallback(self.speak)
        return ask

    def speak(self, msg):
        log.msg('bit.bot.http.request: MessageRequest.speak ',
                self.session_id, msg)
        return self.proto.speak(self.session_id, msg)
