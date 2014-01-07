# ClientInput.py
# The pygame side of the client

import pygame
from sys import exit
from os import environ



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
					KeyProcessor(event.key, client)

				if client.messageNotFinished == False:
					if len(client.chatMessage) < 64:
						client.Message(client.chatMessage)

					elif len(client.chatMessage) < 128:
						#split the message into two lines
						notSplit = True
						position = 64 #- (len(client.user_name) + 4)
						while notSplit == True:
							if client.chatMessage[position] == " ":
								messageA = client.chatMessage[:position]
								messageB = "    " + str(client.chatMessage[position:])
								client.Message(messageA)
								client.Message(messageB, True)
								notSplit = False
							else:
								position -= 1

					elif len(client.chatMessage) < 192:
						#split the message into 2 lines, with messageB containing all of the remainder
						notSplit = True
						position = 64# - (len(client.user_name) + 4)
						while notSplit == True:
							if client.chatMessage[position] == " ":
								messageA = client.chatMessage[:(position)]
								messageB = "    " + str(client.chatMessage[(position):])

								notSplit = False
							else:
								position -= 1
						#split messageB into 2 lines
						notSplit = True
						position = 64 + (len(client.user_name)+4)# - 4 + (len(client.user_name) + 4)
						while notSplit == True:
							if messageB[position] == " ":
								messageBuf = messageB[:(position)]
								messageC = "    " + str(messageB[(position):])
								messageB = messageBuf
								client.Message(messageA)
								client.Message(messageB, True)
								client.Message(messageC, True)
								notSplit = False
							else:
								position -= 1

					elif len(client.chatMessage) < 256:
						#split the message into four lines
						pass
					else:
						client.chatMessage = client.chatMessage[:255]	#cut the message off at 256 characters
						#split the message into four lines

					client.setMessageNotFinished(True)
					client.setChatMessage("")
					
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
				client.setIsCapital(False)
				#print "Shift off"
			if event.key == pygame.K_CAPSLOCK:
				client.setCapsLock(False)
				#print "CapsLock off"



def KeyProcessor(key_pressed, client):
	character = pygame.key.name(key_pressed)
	if character == "`" or character == "left shift" or character == "right shift":
		character = ""

	if client.CapsLock == True:
		character = character.upper()


	if key_pressed == pygame.K_LSHIFT or key_pressed == pygame.K_RSHIFT:		
		client.setIsCapital(True)
		#print "Shift on"

	if character == "caps lock" or character == "CAPS LOCK":
		client.setCapsLock(True)
		#print "CapsLock on"

	if key_pressed == pygame.K_RETURN:
		client.setMessageNotFinished(False)
		

	elif key_pressed == pygame.K_SPACE:
		#if len(client.chatMessage) < 64:
		message = client.chatMessage + " "
		client.setChatMessage(message)

	elif key_pressed == pygame.K_BACKSPACE:
		if client.chatMessage != "":
			message = client.chatMessage[:-1]
			client.setChatMessage(message)

	else:
		if character != "":
			#print isCapital
			if client.isCapital == True:
				character = shiftResolve(character)
				#print "Shift resolved"
			if key_pressed != pygame.K_CAPSLOCK:
				#if len(client.chatMessage) < 64:
				message = client.chatMessage + character
				client.setChatMessage(message)



def shiftResolve(character):

	if character == "/":
		character = "?"
	elif character == "'":
		character = '"'
	elif character == ";":
		character =":"
	elif character == ",":
		character = "<"
	elif character == ".":
		character = ">"
	elif character == "[":
		character = "{"
	elif character == "]":
		character = "}"
	elif character == "\\":
		character = "|"
	elif character == "1":
		character = "!"
	elif character == "2":
		character = "@"
	elif character == "3":
		character = "#"
	elif character == "4":
		character = "$"
	elif character == "5":
		character = "%"
	elif character == "6":
		character = "^"
	elif character == "7":
		character = "&"
	elif character == "8":
		character = "*"
	elif character == "9":
		character = "("
	elif character == "0":
		character = ")"
	elif character == "-":
		character = "_"
	elif character == "=":
		character = "+"
	else:
		character = character.upper()
	
	return character
	