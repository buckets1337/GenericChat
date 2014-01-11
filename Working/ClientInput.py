# ClientInput.py
# The pygame controller side of the client

import pygame
from sys import exit
from os import environ
from time import sleep

import CONFIG
import ChatHandler



def NormalKeyInput(screen, client):

	for event in pygame.event.get():

		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_END or event.type == pygame.QUIT:
			 	exit()

			if event.key == pygame.K_PRINT:
			 	# capture the screen and save it under the date and time in the "screenshots" folder
			 	pass

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
					print client.chatHistoryList
					if len(client.chatHistoryList) > 32:
						client.chatHistoryList.pop(0)
					client.chatHistoryCounter = len(client.chatHistoryList) #- 1
					print "History:" + str(client.chatHistoryCounter) + "History List:" + str(len(client.chatHistoryList))
					if client.chatHistoryCounter > 31:
						client.chatHistoryCounter = 31
					ChatHandler.formatMessage(client)
					client.chatMessage = '|'
					
		if event.type == pygame.KEYUP:

			if client.state == "Chat":

				if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
					client.setIsCapital(False)
					#print "Shift off"

				if event.key == pygame.K_CAPSLOCK:
					client.setCapsLock(False)
					#print "CapsLock off"

			if event.key == pygame.K_F8:
				if client.screenMode == "fullscreen":
					screen = pygame.display.set_mode((CONFIG.SCREEN_WIDTH, CONFIG.SCREEN_HEIGHT))
					client.screenMode = "windowed"
					break
					# x = 0
					# while x < 100:
					# 	sleep(0.01)
					# 	x += 1
					#sleep(1)

				if client.screenMode == "windowed":
					screen = pygame.display.set_mode((CONFIG.SCREEN_WIDTH, CONFIG.SCREEN_HEIGHT), pygame.FULLSCREEN)
					client.screenMode = "fullscreen"
					break
					#sleep(1)







