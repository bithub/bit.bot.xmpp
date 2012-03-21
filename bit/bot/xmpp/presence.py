from wokkel import xmppim


class BotPresence(xmppim.PresenceClientProtocol):

    def __init__(self, streamhost):
        xmppim.PresenceClientProtocol.__init__(self)
        self.streamhost = streamhost
        self.friends_online = set([])

    def connectionInitialized(self):
        xmppim.PresenceClientProtocol.connectionInitialized(self)
        # im avalailable
        self.available()
        #self.available(statuses={None: "Just ask me!"})

    def subscribeReceived(self, entity):
        # im everybody's buddy
        self.subscribed(entity)

    def subscribedReceived(self, entity):
        # somebody is my buddy
        pass

    def unsubscribeReceived(self, entity):
        # if you're not my buddy, then...
        self.unsubscribed(entity)
        self.unsubscribe(entity)

    def availableReceived(self, entity, show=None, statuses=None, priority=0):
        # one of my buddys is online
        self.friends_online.add(entity)

    def unavailableReceived(self, entity, statuses=None):
        # one of my buddys went offline
        print 'unavailbale recieved'
        self.friends_online.remove(entity)
