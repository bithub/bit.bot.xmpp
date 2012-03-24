from zope.interface import Interface as I

from bit.bot.common.interfaces import ISocketRequest

class IJabber(I):
    pass


class IXMPPBotProtocol(I):
    """ curate command """


class IXMPPSocketRequest(ISocketRequest):
    """ an XMPP request object """
