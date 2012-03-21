from zope.interface import implements
from zope.component import getUtility

from bit.core.interfaces import IConfiguration
from bit.bot.common.interfaces import IIntelligent, ISocketRequest


class BitBotRequest(object):
    implements(ISocketRequest)

    def __init__(self, proto):
        self.proto = proto

    @property
    def user(self):
        return self._asker

    @property
    def args(self):
        return self._args

    def speak(self, msg):
        self.proto.speak(self.session_id, msg)

    def ask(self, msg):
        body = str(msg.body)
        mfrom = msg['from']
        self.session_id = msg['from']

        def _respond(response):
            if response:
                self.proto.speak(msg['from'], response)

        domain = getUtility(IConfiguration).get('bot', 'domain')
        if domain == mfrom.split('/')[0].split('@')[1]:
            getUtility(IIntelligent).bot.setPredicate('secure', 'yes', mfrom)

        ask = getUtility(IIntelligent).respond(self, body, mfrom)
        ask.addCallback(_respond)
        return ask
