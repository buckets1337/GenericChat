import sys
import os
from time import sleep, strftime, localtime
from sys import stdin, exit

from PodSixNet.Connection import connection, ConnectionListener
import pygame

import CONFIG

import ClientInput, ClientRenderer

pygame.init()


class GenericClient(ConnectionListener):	

	def __init__(self, host, port):
		#Client.__init__("pygame")
		self.server_name = None
		self.id = None
		self.players = {}
		self.state = "Normal"
		self.CapsLock = False
		self.isCapital = False
		self.chatMessage = ""
		self.messageNotFinished = None
		self.chatBuffer = ["** Chat **"]
		self.user_name = str(sys.argv[2])

		path = str("log/client/" + self.user_name + "/")
		try:
			os.makedirs(path)
		except OSError:
			if not os.path.isdir(path):
				raise

		self.printl("")
		self.printl("----------------------")
		self.printl("GenericClient launched")
		self.printl("----------------------")

		self.printl("Try: " + str(host) + ":" + str(port))
		self.Connect((host, port))


		

		self.printl(">>Connecting as " + self.user_name)
		connection.Send({"action":"SetPlayerName", "user_name":self.user_name})
		

		#Whiteboard.__init__(self)

		#if "connecting" in self.statusLabel:
		#	self.statusLabel = "connecting" + ("." * ((self.frame / 30) % 4))

	def Loop(self, screen):

		self.Pump()
		connection.Pump()
		#print self.state
		ClientRenderer.RenderAll(screen, self)
		ClientInput.NormalKeyInput(self)
		#print self.state
		#return gameState
		#print self.state
		##self.Draw([(self.players[p]['color'], self.players[p]['lines']) for p in self.players])

		# still need a call to the draw function here

	#######################	
	### Setters ###
	#######################
	def setState(self, state):
		self.state = state

	def setCapsLock(self, state):
		self.CapsLock = state

	def setIsCapital(self, state):
		self.isCapital = state

	def setChatMessage(self, message):
		self.chatMessage = message

	def setMessageNotFinished(self, state):
		self.messageNotFinished = state


	###############################
	### Network event callbacks ###
	###############################
	def Network_SetServerName(self, data):
		self.server_name = data['name']
		self.printl("Connected to", self.server_name, "at " + sys.argv[1])
		self.printl(" ")

	def Network_SetPlayerId(self, data):
		self.id = data['id']
		#print "Player ID:", self.id

	def Network_GetUserName(self, data):
		connection.Send({"action":"SetPlayerName", "user_name":self.user_name})

	def Network_DisplayMessage(self, data):
		message = "**<system>: " + data['message']
		self.printl(message)
		self.chatBuffer.append(message)
		#self.printl("")

	def Network_Message(self, data):
		message = data['message']
		self.printl(message)
		self.chatBuffer.append(message)


	#######################
	### Utility Methods ###
	#######################
	def GetUserName(self):
		return self.user_name

	def Message(self, message, stripLabel=False):
		connection.Send({"action":"Message", "message":message, "user_name":self.user_name, "stripLabel":stripLabel})

	def printl(self, message):
		timeStamp = strftime("%d %b %Y %H:%M:%S",localtime() )
		logName = strftime("%d_%m_%Y",localtime())

		print str(message)

		if message != '':
			logEntry = "<" + str(timeStamp) + ">: " + str(message)
		else:
			logEntry = str(message)
		logLocation = str('log/client/' + self.user_name + "/" + logName + '.log')
		log = open(logLocation, 'a')
		log.write(logEntry + "\n")
		log.close()

	def printScreen(screen, message):
		pass


	# built in stuff
	def Network(self, data):
		#print 'network:', data
		pass
	
	def Network_connected(self, data):
		self.printl("**Connection Established**")
		self.printl("")
	
	def Network_error(self, data):
		self.printl('error: ' + data['error'][1])
		connection.Close()
	
	def Network_disconnected(self, data):
		self.printl('Server disconnected')
		exit()

	


if len(sys.argv) != 3:
	print "Usage:", sys.argv[0], "host:port", "user_name"
	print "e.g.", sys.argv[0], "localhost:31425", "JohnDoe"
else:
	host, port = sys.argv[1].split(":")
	client = GenericClient(host, int(port))
	screen = pygame.display.set_mode((CONFIG.SCREEN_WIDTH, CONFIG.SCREEN_HEIGHT))
	#print client.state
	while 1:
		client.Loop(screen)
		#print client.state
		sleep(0.001)
