import json

from zope.interface import implements
from zope.component import getUtility, queryAdapter

from twisted.python import log

from bit.core.interfaces import IConfiguration, ICommand
from bit.bot.common.interfaces import IIntelligent, ISubscribe
from bit.bot.xmpp.interfaces import IXMPPSocketRequest


class XMPPMessageRequest(object):
    implements(IXMPPSocketRequest)

    def __init__(self, proto):
        self.proto = proto

    def response(self, msg):
        log.msg('bit.bot.xmpp.request: MessageRequest.response: ', msg)
        self.proto.transport.write(json.dumps(msg))

    def load(self, sessionid, msg):
        log.msg('bit.bot.xmpp.request: MessageRequest.load: ',
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
        log.msg('bit.bot.xmpp.request: MessageRequest.speak ',
                self.session_id, msg)
        return self.proto.speak(self.session_id, msg)


class XMPPCommandRequest(object):
    implements(IXMPPSocketRequest)

    def __init__(self, proto):
        self.proto = proto

    def response(self, msg):
        log.msg('bit.bot.xmpp.request: CommandRequest.response: ', msg)
        self.proto.transport.write(json.dumps(msg))

    def load(self, sessionid, msg):
        log.msg('bit.bot.xmpp.request: CommandRequest.load: ',
                sessionid, msg)
        self.session_id = sessionid

        command_name = msg.strip().split(' ')[0]
        command = queryAdapter(self, ICommand, command_name)
        self.session_id = sessionid
        if not command:
            command = queryAdapter(self, ICommand)
            msg = 'help %s' % command_name
        return command.load(sessionid, msg).addCallback(self.speak)

    def speak(self, msg):
        log.msg('bit.bot.xmpp.request: CommandRequest.speak ',
                self.session_id, msg)
        return self.proto.speak(self.session_id, msg)


class XMPPSubscribeRequest(object):
    implements(IXMPPSocketRequest)

    def __init__(self, proto):
        self.proto = proto

    def response(self, msg):
        log.msg('bit.bot.xmpp.request: SubscribeRequest.response: ', msg)
        self.proto.transport.write(json.dumps(msg))

    def load(self, sessionid, msg):
        log.msg('bit.bot.xmpp.request: SubscribeRequest.load: ',
                sessionid, msg)
        self.session_id = sessionid
        subscribe = queryAdapter(self, ISubscribe, msg.strip().split(' ')[0])
        self.session_id = sessionid
        return subscribe.load(sessionid, msg).addCallback(self.speak)

    def speak(self, msg):
        log.msg('bit.bot.xmpp.request: SubscribeRequest.speak ',
                self.session_id, msg)
        return self.proto.speak(self.session_id, msg)
