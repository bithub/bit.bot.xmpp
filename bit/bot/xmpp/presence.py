from twisted.python import log

from wokkel import xmppim


class BotPresence(xmppim.PresenceClientProtocol):

    def __init__(self, streamhost):
        xmppim.PresenceClientProtocol.__init__(self)
        self.streamhost = streamhost
        self.friends_online = set([])

    def connectionInitialized(self):
        log.msg('bit.bot.xmpp.presence: BotPresence.connectionInitialized')
        xmppim.PresenceClientProtocol.connectionInitialized(self)
        # im avalailable
        self.available()
        #self.available(statuses={None: "Just ask me!"})

    def subscribeReceived(self, entity):
        log.msg('bit.bot.xmpp.presence: BotPresence.subscribeReceived: ', entity)
        # im everybody's buddy
        self.subscribed(entity)

    def subscribedReceived(self, entity):
        log.msg('bit.bot.xmpp.presence: BotPresence.subscribedReceived: ', entity)
        # somebody is my buddy
        pass

    def unsubscribeReceived(self, entity):
        log.msg('bit.bot.xmpp.presence: BotPresence.unsubscribeReceived: ', entity)
        # if you're not my buddy, then...
        self.unsubscribed(entity)
        self.unsubscribe(entity)

    def availableReceived(self, entity, show=None, statuses=None, priority=0):
        log.msg('bit.bot.xmpp.presence: BotPresence.availableReceived: ', entity)
        # one of my buddys is online
        self.friends_online.add(entity)

    def unavailableReceived(self, entity, statuses=None):
        log.msg('bit.bot.xmpp.presence: BotPresence.unavailableReceived', entity)
        # one of my buddys went offline
        print 'unavailbale recieved'
        self.friends_online.remove(entity)
