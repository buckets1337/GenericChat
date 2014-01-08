# ClientInput.py
# The pygame controller side of the client

import pygame
from sys import exit
from os import environ

import ChatHandler



def NormalKeyInput(client):

	for event in pygame.event.get():

		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_END or event.type == pygame.QUIT:
			 	exit()

			if client.state == "Normal":
				if event.key == pygame.K_BACKQUOTE:
					client.setState("Chat")
					client.setChatMessage("")
					client.setMessageNotFinished(True)
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
					ChatHandler.formatMessage(client)
					
		if event.type == pygame.KEYUP:

			if client.state == "Chat":

				if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
					client.setIsCapital(False)
					#print "Shift off"

				if event.key == pygame.K_CAPSLOCK:
					client.setCapsLock(False)
					#print "CapsLock off"






