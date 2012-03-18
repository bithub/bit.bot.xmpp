

from zope.interface import implements
from zope.component import getGlobalSiteManager,getUtility

from twisted.words.xish import domish

from bit.bot.common.interfaces import IGroups, IMember, IGroup

from wokkel.xmppim import MessageProtocol, AvailablePresence

from bit.bot.base.roles import RoleProvider
from bit.bot.xmpp.request import BitBotRequest

from bit.bot.common.interfaces import IGroupOfPeople, IMembers, IBotRequest, ICurateBotProtocol, IMemory, IRoles

from bit.core.interfaces import IConfiguration


class BotProtocol(MessageProtocol):
    implements(ICurateBotProtocol)
    
    def __init__(self):
        super(MessageProtocol,self).__init__()
        #return
    

        #from ldaptor.interfaces import ILDAPEntry
        #from trinity.curate.ldap.network_members import NetworkMembers, NetworkMember
        #from trinity.curate.ldap.network_groups import NetworkGroups, NetworkGroup
        
        #from trinity.curate.db.memory import MySQLMemory
        
        gsm = getGlobalSiteManager()

        gsm.registerUtility(self
                            ,ICurateBotProtocol
                            )


        gsm.registerAdapter(BitBotRequest
                            ,(ICurateBotProtocol,)
                            ,IBotRequest
                            )

        return

        members = NetworkMembers(self)

        gsm.registerAdapter(NetworkMember
                            ,(IMembers,ILDAPEntry)
                            ,IMember
                            )

        gsm.registerAdapter(NetworkGroup
                            ,(IGroups,ILDAPEntry)
                            ,IGroup
                            )
        

        
        groups  = NetworkGroups(self)        

        memory = MySQLMemory(self)
        gsm.registerUtility(memory
                            ,IMemory
                            )

        gsm.registerUtility(groups
                            ,IGroups
                            )

        gsm.registerUtility(members
                            ,IMembers
                            )
        gsm.registerUtility(members
                            ,IGroupOfPeople
                            ,'members'
                            )
        gsm.registerUtility(RoleProvider(self)
                            ,IRoles
                            )
            
    def connectionMade(self):
        print "Connected!"
        # send initial presence
        self.send(AvailablePresence())

    def connectionLost(self, reason):
        print "Disconnected!"

    def speak(self,recip,resp):
        reply = domish.Element((None, "message"))
        config = getUtility(IConfiguration)
        reply["to"] = recip
        reply["from"] = config.get('bot', 'jid')
        reply["type"] = 'chat'        
        reply.addElement("body", content=resp)
        self.send(reply)

    def presence(self,pres):        
        presence = domish.Element(('jabber:client', 'presence'))
        for k,v in pres.items():
            presence[k] = v
        self.send(presence)
      
    def subscribe(self,recip):
        pres = {}
        pres['to'] = recip
        pres['type'] = 'subscribe'
        return self.presence(pres)
            
    def onAnswer(self,resp,request):
        self.speak(request.user,resp)

    def onMessage(self, msg):
        if msg["type"] == 'chat' and hasattr(msg, "body") and msg.body:
            request = IBotRequest(self)
            request.ask(msg)
