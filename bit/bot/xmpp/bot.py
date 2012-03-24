from zope.interface import implements
from zope.component import getUtility, getAdapter

from twisted.python import log
from twisted.words.xish import domish

from wokkel.xmppim import MessageProtocol, AvailablePresence

from bit.core.interfaces import IConfiguration
from bit.bot.common.interfaces import ISocketRequest
from bit.bot.xmpp.interfaces import IXMPPBotProtocol


class XMPPBotProtocol(MessageProtocol):
    implements(IXMPPBotProtocol)

    def __init__(self):
        super(MessageProtocol, self).__init__()

    def connectionMade(self):
        log.msg('bit.bot.xmpp.bot: BotProtocol.connectionMade')
        # im online!
        self.send(AvailablePresence())

    def connectionLost(self, reason):
        log.msg('bit.bot.xmpp.bot: BotProtocol.connectionLost')
        # im offline!
        print "Disconnected!"

    def speak(self, recip, resp):
        log.msg('bit.bot.xmpp.bot: BotProtocol.speak')
        reply = domish.Element((None, "message"))
        config = getUtility(IConfiguration)
        reply["to"] = recip
        reply["from"] = config.get('xmpp', 'jid')
        reply["type"] = 'chat'
        reply.addElement("body", content=resp)
        self.send(reply)

    def presence(self, pres):
        log.msg('bit.bot.xmpp.bot: BotProtocol.presence')
        presence = domish.Element(('jabber:client', 'presence'))
        for k, v in pres.items():
            presence[k] = v
        self.send(presence)

    def subscribe(self, recip):
        log.msg('bit.bot.xmpp.bot: BotProtocol.subscribe')
        pres = {}
        pres['to'] = recip
        pres['type'] = 'subscribe'
        return self.presence(pres)

    def onAnswer(self, resp, request):
        log.msg('bit.bot.xmpp.bot: BotProtocol.onAnswer', resp)
        self.speak(request.user, resp)

    def onMessage(self, msg):
        log.msg('bit.bot.xmpp.bot: BotProtocol.onMessage', msg)
        if msg["type"] == 'chat' and hasattr(msg, "body") and msg.body:
            message = str(msg.body)
            if message.startswith('>'):
                request = getAdapter(self, ISocketRequest, name="command")
                message = message[1:]
            elif message.startswith('~'):
                request = getAdapter(self, ISocketRequest, name="subscribe")
                message = message[1:]
            else:
                request = getAdapter(self, ISocketRequest, name="message")
            request.load(msg['from'], message)
