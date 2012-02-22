
from zope.interface import implements
from zope.component import getUtility


from twisted.words.protocols.jabber.jid import JID

from wokkel import client

from bit.core.interfaces import IPlugin, IConfiguration, IServices

from bit.bot.common.interfaces import IJabber
from bit.bot.base.plugin import BotPlugin

