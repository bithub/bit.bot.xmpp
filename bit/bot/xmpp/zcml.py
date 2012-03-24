import zope
import bit

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('bit.bot.xmpp')


class IXMPPDirective(zope.interface.Interface):
    """
    Define a xmpp
    """
    name = zope.schema.TextLine(
        title=_("Name"),
        description=_("The xmpp name"),
        required=True,
        )
    parent = zope.schema.TextLine(
        title=_("Name"),
        description=_("The service parent"),
        required=True,
        )
    factory = zope.configuration.fields.GlobalObject(
        title=_("XMPP factory"),
        description=_("The xmpp factory"),
        required=True,
        )


def xmpp(_context, parent, name, factory):
    services = zope.component.getUtility(bit.core.interfaces.IServices)
    _xmpps = {name: factory()}
    _context.action(
        discriminator=None,
        callable=services.add,
        args=(parent, _xmpps)
        )
