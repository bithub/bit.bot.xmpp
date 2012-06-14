from zope.interface import implementer
from zope.component import getUtility

from twisted.words.protocols.jabber.jid import JID

from wokkel import client

from bit.core.interfaces import IConfiguration
from bit.bot.xmpp.interfaces import IJabber, IXMPPBotProtocol
from bit.bot.xmpp.presence import BotPresence


@implementer(IJabber)
def botXMPP():
    configuration = getUtility(IConfiguration)
    bot_jid = JID(configuration.get('xmpp', 'jid'))
    password = configuration.get('passwords', 'xmpp')
    return client.XMPPClient(bot_jid, password)


def botFactory():
    bot = getUtility(IJabber)
    protocol = getUtility(IXMPPBotProtocol)
    presence = BotPresence(protocol)
    protocol._presence = presence
    protocol.setHandlerParent(bot)
    presence.setHandlerParent(bot)
    presence.available()
    return bot
