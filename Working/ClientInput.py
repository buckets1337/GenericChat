# ClientInput.py
# The pygame controller side of the client

import pygame
from sys import exit
from os import environ
from time import sleep, strftime, localtime

import CONFIG
import ChatHandler



def NormalKeyInput(screen, client):

	for event in pygame.event.get():

		if event.type == pygame.KEYDOWN:

			#print "KEYDOWN"

			if event.key == pygame.K_END or event.type == pygame.QUIT:
			 	exit()


			if event.key == pygame.K_PRINT:
			 	# capture the screen and save it under the date and time in the "screenshots" folder
			 	timeStamp = strftime("%d_%m_%Y_%Hh%Mm%Ss",localtime() )
			 	location = str("screenshots/" + client.user_name + "/" + timeStamp + ".jpeg")
			 	pygame.image.save(screen, location)
			 	client.printl("Screenshot saved as \"" + location + "\"")
			 	


			if event.key == pygame.K_F8:

				#print client.screenMode

				if (client.screenMode == "fullscreen" and CONFIG.SCREEN_MODE == "fullscreen") or (client.screenMode == "windowed" and CONFIG.SCREEN_MODE == "windowed"):
					screen = pygame.display.set_mode((CONFIG.SCREEN_WIDTH, CONFIG.SCREEN_HEIGHT))
					if CONFIG.SCREEN_MODE == "fullscreen":
						client.screenMode = "windowed"
					elif CONFIG.SCREEN_MODE == "windowed":
						client.screenMode = "fullscreen"


				elif (client.screenMode == "windowed" and CONFIG.SCREEN_MODE == "fullscreen") or (client.screenMode == "fullscreen" and CONFIG.SCREEN_MODE == "windowed"):
					screen = pygame.display.set_mode((CONFIG.SCREEN_WIDTH, CONFIG.SCREEN_HEIGHT), pygame.FULLSCREEN)
					if CONFIG.SCREEN_MODE == "fullscreen":
						client.screenMode = "fullscreen"
					elif CONFIG.SCREEN_MODE == "windowed":
						client.screenMode = "windowed"

			if client.state == "Normal":

				if event.key == pygame.K_BACKQUOTE:
					client.setState("Chat")
					client.setChatMessage("")
					client.setMessageNotFinished(True)
					client.chatCharacterCounter = 0
					client.chatCursorLocation = 0
					print ""
					print ">> chatting..."


			if client.state == "Chat":

				if event.key == pygame.K_ESCAPE:
					client.setState("Normal")
					print ">> done chatting."

				if client.messageNotFinished == True:
					# have not yet hit enter, so keep adding to the message
					ChatHandler.keyProcessor(event.key, client)

				if client.messageNotFinished == False:
					# have hit enter, format and send the message
					client.chatHistoryList.append(client.chatMessage)
					#print client.chatHistoryList
					if len(client.chatHistoryList) > 32:
						client.chatHistoryList.pop(0)
					client.chatHistoryCounter = len(client.chatHistoryList) #- 1
					#print "History:" + str(client.chatHistoryCounter) + "History List:" + str(len(client.chatHistoryList))
					if client.chatHistoryCounter > 31:
						client.chatHistoryCounter = 31
					ChatHandler.formatMessage(client)
					client.chatMessage = '|'
					


		if event.type == pygame.KEYUP:

			#print "KEYUP"

			if client.state == "Chat":

				if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
					client.setIsCapital(False)
					#print "Shift off"


				if event.key == pygame.K_CAPSLOCK:
					client.setCapsLock(False)
					#print "CapsLock off"

			





