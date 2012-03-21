from zope.interface import implementer
from zope.component import getUtility

from twisted.words.protocols.jabber.jid import JID

from wokkel import client

from bit.core.interfaces import IConfiguration
from bit.bot.common.interfaces import IJabber
from bit.bot.xmpp.presence import BotPresence
from bit.bot.xmpp.bot import BotProtocol


@implementer(IJabber)
def botXMPP():
    configuration = getUtility(IConfiguration)
    bot_jid = JID(configuration.get('bot', 'jid'))
    password = configuration.get(
        'passwords', configuration.get('bot', 'password'))
    return client.XMPPClient(bot_jid, password)


def botFactory():
    bot = getUtility(IJabber)
    curatebot = BotProtocol()
    presence = BotPresence(curatebot)
    curatebot._presence = presence
    curatebot.setHandlerParent(bot)
    presence.setHandlerParent(bot)
    presence.available()
    return bot
