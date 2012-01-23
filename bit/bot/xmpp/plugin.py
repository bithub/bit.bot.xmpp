
from zope.interface import implements
from zope.component import getUtility
from bit.bot.common.interfaces import IPlugin


from twisted.words.protocols.jabber.jid import JID

from wokkel import client

from bit.bot.common.interfaces import IConfiguration, IJabber, IServices
from bit.bot.base.plugin import BotPlugin

from bit.bot.xmpp.presence import BotPresence
from bit.bot.xmpp.bot import BotProtocol


class BotXMPP(BotPlugin):
    implements(IPlugin)
    name = 'bit.bot.xmpp'


    @property
    def utils(self):
        configuration = getUtility(IConfiguration)        
        bot_jid = JID(configuration.get('bot','jid'))
        password = configuration.get('bot','password')                        
        return [(client.XMPPClient(bot_jid, password),IJabber)]
        
    def load_services(self):        
        bot = getUtility(IJabber)
        curatebot = BotProtocol()        
        presence = BotPresence(curatebot)
        curatebot._presence = presence
        curatebot.setHandlerParent(bot)    
        presence.setHandlerParent(bot)
        presence.available()
        getUtility(IServices).add('bit.bot.xmpp', {'bot': bot})
