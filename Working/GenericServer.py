from time import sleep, localtime, strftime
from weakref import WeakKeyDictionary
from time import time
import sys

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

#import pygame



class GenericChannel(Channel):
	"""
	This is the server representation of a single connected client.
	"""
	def __init__(self, *args, **kwargs):
		Channel.__init__(self, *args, **kwargs)
		self.id = self._server.NextId()
		self.user_name = None 	

		

	def PassOn(self, data):
		# pass on what we received to all connected clients
		data.update({"id": self.id})
		self._server.SendToAll(data)

	
	def Close(self):
		self._server.printl('')
		self._server.printl(self)
		self._server.printl('Player disconnected >> "' + self.user_name + '"')
		self._server.DelPlayer(self)
	
	##################################
	### Network specific callbacks ###
	##################################

	def Network_SetPlayerName(self, data):
		timeStamp = strftime("%d %b %Y %H:%M:%S",localtime() )
		self.user_name = data['user_name']
		self._server.printl("Player ID:" + str(self.id) + " set as \"" + self.user_name +"\"")
		self._server.printl('')
		self._server.SendToAll({"action":"DisplayMessage", "message":str("(" + timeStamp + ") >> " +self.user_name + " connected.")})
		self._server.DisplayMessage(self, "Hello, " + self.user_name + "!")

	def Network_Message(self, data):
		nickname = str(data['user_name'])
		if data['stripLabel'] == False:
			messageString = "(" + nickname + "): " + data['message']
		elif data['stripLabel'] == True:
			messageString = data['message']
		self._server.printl(messageString)
		self._server.SendToAll( {"action":"Message", "message":messageString} )





class GenericServer(Server):
	channelClass = GenericChannel
	
	def __init__(self, *args, **kwargs):
		Server.__init__(self, *args, **kwargs)
		self.id = 0 	#counter for assigning IDs to connected clients
		self.players = WeakKeyDictionary()
		self.name = sys.argv[2]

		self.printl('')
		self.printl('----------------------')
		self.printl('GenericServer launched')
		self.printl('----------------------')
		self.printl('>> Welcome to ' + self.name)
		self.printl('')
	
	def Connected(self, channel, addr):
		self.printl('')
		self.printl(channel)
		self.printl("New Channel connected >> " + str(addr))
		channel.Send({"action":"SetServerName ", "name":str(self.name)})
		channel.Send({"action":"SetPlayerId", "id": self.id})
		self.addPlayer(channel)

		
	def addPlayer(self, player):
		self.printl(">>New Player" + str(player.addr) + " assigned ID: " + str(player.id))
		self.players[player] = True
		#player.Send({"action": "initial", "lines": dict([(p.id, {"color": p.color, "lines": p.lines}) for p in self.players])})		#notifies all connected players of new player's initial state.  needs to be modified to fit my specifics
		#self.SendPlayers()	#update the 'players' list for all connected players

	def DelPlayer(self, player):
		timeStamp = timeStamp = strftime("%d %b %Y %H:%M:%S",localtime() )
		self.printl("Deleting Channel" + str(player.addr) + " >> \"" + str(player.user_name) +"\"")
		self.SendToAll({"action":"DisplayMessage", "message":str("(" + timeStamp + ") >> " + player.user_name) + " disconnected"})
		del self.players[player]
		#self.SendPlayers()

	# def SendPlayers(self):		# sends list of players to all players	Needs to be modified for my code
	# 	self.SendToAll({"action": "players", "players": dict([(p.id, p.user_name) for p in self.players])})		

	def SendToAll(self, data):		# sends <data> to all connected players
		[p.Send(data) for p in self.players]

	def DisplayMessage(self, player, message):
		player.Send({"action":"DisplayMessage", "message":str(message)})

	def NextId(self):		# increments the id counter, then grabs the next client ID and returns it
		self.id += 1
		return self.id

	def GetName(self):
		return self.name

	def printl(self, message):
		timeStamp = strftime("%d %b %Y %H:%M:%S",localtime() )
		logName = strftime("%d_%m_%Y",localtime())
		print str(message)
		if message != '':
			logEntry = "<" + str(timeStamp) + ">: " + str(message)
		else:
			logEntry = str(message)
		logLocation = str('log/server/' + logName + '.log')
		log = open(logLocation, 'a')
		log.write(logEntry + "\n")
		log.close()

	

	def Launch(self):		# run the server
		while True:
			self.Pump()
			sleep(0.0001)



# get command line argument of server, port
if len(sys.argv) != 3:
	print "Usage:", sys.argv[0], "host:port", "server_name"
	print "e.g.", sys.argv[0], "localhost:31425", "MyServer"
else:
	host, port = sys.argv[1].split(":")
	server = GenericServer(localaddr=(host, int(port)))
	server.Launch()

