from time import sleep, localtime, strftime
from weakref import WeakKeyDictionary
from time import time
import sys
import os
from sys import stdin, exit
import pickle

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

from passlib.context import CryptContext

import GetPassword



passwordCryptContext = CryptContext(schemes=["pbkdf2_sha512", "sha512_crypt"], default="sha512_crypt")


class GenericChannel(Channel):
	"""
	This is the server representation of a single connected client.
	"""
	def __init__(self, *args, **kwargs):
		Channel.__init__(self, *args, **kwargs)
		self.id = self._server.NextId()
		self.user_name = None
		self.num_attempts = 0


	def PassOn(self, data):
		# pass on <data> to all connected clients, with self.id now attached
		data.update({"id": self.id})
		self._server.SendToAll(data)
	

	def Close(self):
		# close the channel
		self._server.printl('')
		self._server.printl(self)
		self._server.printl('Player disconnected >> "' + str(self.user_name) + '"')
		self._server.DelPlayer(self)
		#self._server.ExitClient(self)
	
	##################################
	### Network specific callbacks ###
	##################################

	def Network_closeConnection(self, player):
		self._server.ExitClient(self)


	def Network_SetPlayerName(self, data):
		# Get the server to assign an id to the username when connecting

		self.user_name = data['user_name']


	def Network_Greeting(self):

		timeStamp = strftime("%d %b %Y %H:%M:%S",localtime() )

		if len(self.user_name)>12:
			display_name = self.user_name[:12]
			display_name += "... "
		else:
			display_name = self.user_name

		self._server.printl("Player ID:" + str(self.id) + " set as \"" + self.user_name +"\"")
		self._server.printl('')
		self._server.SendToAll({"action":"DisplayMessage", "message":str("(" + timeStamp + ") >> " + display_name + " connected.")})
		self._server.DisplayMessage(self, "Hello, " + self.user_name + "!")


	def Network_Message(self, data):
		# send a chat message to the server and all clients
		nickname = str(data['user_name'])
		if data['stripLabel'] == False:
			messageString = "(" + nickname + "): " + data['message']
		elif data['stripLabel'] == True:
			messageString = data['message']
		self._server.printl(messageString)
		self._server.SendToAll( {"action":"Message", "message":messageString} )


	def Network_CheckUsernameExists(self, data):
		verify = self._server.CheckUsernameExists(str(data['user_name']))
		if verify == True:
			self._server.SendData(self, {"action":"ReturningUser"})
		if verify == False:
			self._server.SendData(self, {"action":"NewUser"})


	def Network_CheckPassword(self, data):
		# checks if the password entered is correct, and if so, send a "verify success" to the client

		if self._server.CheckUsernameExists(str(data['user_name'])):

			self._server.printl("Verifying password for " + str(self.id) + ": " + data['user_name'] + "...")
			#self._server.DisplayConsoleMessage(self, "Verifying password for " + str(self.id) + ": " + data['user_name'] + "...")

			# have the server check the password against it's "passwordHash" file
			passwordCorrect = self._server.checkHashedPassword(data['user_name'], data['password'])
			if passwordCorrect:
				# continue connecting
				self._server.printl("...password correct. (" + self.user_name + ")")
				self._server.StartClient(self)
				self.Network_Greeting()
				return

			else:
				if self.num_attempts < 5:
					self.num_attempts += 1
					self._server.DisplayConsoleMessage(self, "Incorrect Password.")
					self._server.printl(str(5 - self.num_attempts) + " attempts remaining. (" + self.user_name + ")")
					self._server.GetPassword(self)
				else:
					self._server.DisplayConsoleMessage(self, "Too many failed attempts, disconnecting.")
					self._server.DisconnectPlayer(self)
					#self._server.DelPlayer(self)


	def Network_SetPassword(self, data):
		#sets the password for the player
		self._server.updatePasswordHash(self.user_name, data['password'])

		self._server.DisplayConsoleMessage(self, "Password set.")
		self._server.StartClient(self)
		self.Network_Greeting()


	def Network_NewUser(self, data):
		# sets up a new user
			self._server.DisplayConsoleMessage(self, "A new user!")
			self._server.GetUserPassword(self)









class GenericServer(Server):
	channelClass = GenericChannel
	
	def __init__(self, *args, **kwargs):
		Server.__init__(self, *args, **kwargs)
		self.id = 0 	#counter for assigning IDs to connected clients
		self.players = WeakKeyDictionary()
		self.name = sys.argv[2]
		self.passwordHash = {"none":"none"}

		path = [str("log/server/" + self.name + "/"), str("serverData/" + self.name + "/")]

		for pathname in path:
			try:
				os.makedirs(pathname)
			except OSError:
				if not os.path.isdir(pathname):
					raise

		self.printl('')
		self.printl('----------------------')
		self.printl('GenericServer launched')
		self.printl('----------------------')
		self.printl('>> Welcome to ' + str(self.name))
		self.printl('')

		#print self.passwordHash
		self.openPasswordHash()


	def SendData(self, channel, data):
		channel.Send(data)


	def ExitClient(self, player):
		player.Send({"action":"Exit"})


	def StartClient(self, player):
		player.Send({"action":"SetVerify"})
	

	def Connected(self, channel, addr):
		# runs each time a client connects
		self.printl('')
		self.printl(channel)
		self.printl("New Channel connected >> " + str(addr))
		channel.Send({"action":"SetServerName ", "name":str(self.name)})
		channel.Send({"action":"SetPlayerId", "id": self.id})
		self.addPlayer(channel)


	def openPasswordHash(self):
		# opens the "passwordHash" file and saves it to the self.passwordHash dictionary
		passwordHashFile = open('serverData/' + str(self.name) + '/passwordHash', 'a+b')
		passwordHashFile.seek(0)

		openingBits = passwordHashFile.read(4)

		if openingBits != '':

			lineNo = 0
			for line in passwordHashFile:
				feed = line
				#print feed
				if lineNo > 0:
					key, value = feed.split(':')
					value = value[:-1]
					#print "key:" + key + " value:" + value
					self.passwordHash[key] = value
				lineNo += 1
				#print self.passwordHash
		else:

			for entry in self.passwordHash:
				passwordHashFile.write(entry + ":" + self.passwordHash[entry] + '\n')
			passwordHashFile.close()

		# close the passwordHash file
		passwordHashFile.close()
		

	def updatePasswordHash(self, username, password):
		# # removes the old passwordHash file
		os.remove("serverData/" + str(self.name) + "/passwordHash")
		# opens a fresh "passwordHash" file
		passwordHashFile = open("serverData/" + str(self.name) + "/passwordHash", 'a+b')
		passwordHashFile.seek(0)
		# appends a new PasswordHash to self.passwordHash
		passwordHash = passwordCryptContext.encrypt(password)
		self.passwordHash[username] = passwordHash

		for entry in self.passwordHash:
			passwordHashFile.write(entry + ":" + self.passwordHash[entry] + '\n')


		# closes the passwordHash file
		passwordHashFile.close()


	def addPlayer(self, player):
		# add the new client to the list of players
		self.printl(">>New Player" + str(player.addr) + " assigned ID: " + str(player.id))
		self.players[player] = True
		#player.Send({"action": "initial", "lines": dict([(p.id, {"color": p.color, "lines": p.lines}) for p in self.players])})		#notifies all connected players of new player's initial state.  needs to be modified to fit my specifics
		#self.SendPlayers()	#update the 'players' list for all connected players


	def DelPlayer(self, player):
		# remove a client from the list of players on disconnect
		timeStamp = timeStamp = strftime("%d %b %Y %H:%M:%S",localtime() )

		display_name = player.user_name
		if len(player.user_name) > 12:
			display_name = display_name[:12]
			display_name += "... "

		self.printl("Deleting Channel" + str(player.addr) + " >> \"" + str(player.user_name) +"\"")
		#self.printl("")
		self.SendToAll({"action":"DisplayMessage", "message":str("(" + timeStamp + ") >> " + display_name) + " disconnected"})
		# print player
		# print self.players[player]
		del self.players[player]
		#self.SendPlayers()


	def DisconnectPlayer(self, player):
		# kicks a player
		player.Send({"action":"disconnect"})
		#player.Close()


	def SendPlayers(self):		
		# sends list of players to all players	Might need to be adjusted
	 	self.SendToAll({"action": "players", "players": dict([(p.id, p.user_name) for p in self.players])})		


	def SendToAll(self, data):		
		# sends <data> to all connected players
		[p.Send(data) for p in self.players]


	def DisplayMessage(self, player, message):
		player.Send({"action":"DisplayMessage", "message":str(message)})


	def DisplayConsoleMessage(self, player, message):
		player.Send({"action":"ConsoleMessage", "message":str(message)})


	def NextId(self):		
		# increments the id counter, then grabs the next client ID and returns it
		self.id += 1
		return self.id


	def checkHashedPassword(self, username, password):
		
		#print " " + password + " "
		# check the hashed password against the entry for the username.  If they are the same, move on
		passwordCorrect = passwordCryptContext.verify(password, self.passwordHash[username])

		return passwordCorrect


	def CheckUsernameExists(self, username):
		# check if a hashed username is in self.passwordHash
		#print "UN" + username
		if username in self.passwordHash:
			return True
		else:
			return False


	def GetUserPassword(self, player):
		# gets a password over the network from the user for registration
		player.Send({"action":"GetUserPassword"})


	def GetPassword(self, player):
		# gets another password attempt from the user
		player.Send({"action":"GetPassword"})


	def GetName(self):
		return self.name


	def printl(self, message):
		# print to the console and the log
		timeStamp = strftime("%d %b %Y %H:%M:%S",localtime() )
		logName = strftime("%d_%m_%Y",localtime())
		print str(message)
		if message != '':
			logEntry = "<" + str(timeStamp) + ">: " + str(message)
		else:
			logEntry = str(message)
		logLocation = str('log/server/' + self.name + "/" + logName + '.log')
		#need to check if the file exists before opening, and if not, need to create it first or else it throws an error on Windows
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

