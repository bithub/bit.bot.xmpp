from zope.interface import implements
from zope.component import getGlobalSiteManager, getUtility

from twisted.words.xish import domish

from wokkel.xmppim import MessageProtocol, AvailablePresence

from bit.bot.xmpp.request import BitBotRequest
from bit.bot.common.interfaces import IBotRequest, ICurateBotProtocol
from bit.core.interfaces import IConfiguration


class BotProtocol(MessageProtocol):
    implements(ICurateBotProtocol)

    def __init__(self):
        super(MessageProtocol, self).__init__()

        gsm = getGlobalSiteManager()

        gsm.registerUtility(self,
                            ICurateBotProtocol
                            )

        gsm.registerAdapter(BitBotRequest,
                            (ICurateBotProtocol, ),
                            IBotRequest
                            )

    def connectionMade(self):
        print "Connected!"
        # send initial presence
        self.send(AvailablePresence())

    def connectionLost(self, reason):
        print "Disconnected!"

    def speak(self, recip, resp):
        reply = domish.Element((None, "message"))
        config = getUtility(IConfiguration)
        reply["to"] = recip
        reply["from"] = config.get('bot', 'jid')
        reply["type"] = 'chat'
        reply.addElement("body", content=resp)
        self.send(reply)

    def presence(self, pres):
        presence = domish.Element(('jabber:client', 'presence'))
        for k, v in pres.items():
            presence[k] = v
        self.send(presence)

    def subscribe(self, recip):
        pres = {}
        pres['to'] = recip
        pres['type'] = 'subscribe'
        return self.presence(pres)

    def onAnswer(self, resp, request):
        self.speak(request.user, resp)

    def onMessage(self, msg):
        if msg["type"] == 'chat' and hasattr(msg, "body") and msg.body:
            request = IBotRequest(self)
            request.ask(msg)
