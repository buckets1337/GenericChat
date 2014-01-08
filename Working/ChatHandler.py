#ChatHandler.py
#Handles chat message functionality and formatting

import pygame
from os import environ

def formatMessage(client):
	messageList = []
	## This next section works, but is a repetitive mess and should be rewritten to avoid repetition
	# Splits client.chatMessage into up to 4 lines based on length, and sends them as separate messages so they show up on separate lines
	if len(client.chatMessage) < (64 - (len(client.user_name)+4)):
		messageList.append(client.chatMessage)
		sendMessage(messageList, client)

	elif len(client.chatMessage) < (128 - (len(client.user_name)+4)):
		splitLines(client.chatMessage, messageList, False, client)
		sendMessage(messageList, client)
		

	elif len(client.chatMessage) < 192:
		splitLines(client.chatMessage, messageList, False, client)
		splitLines(messageList[1], messageList, True, client)
		sendMessage(messageList, client)

	elif len(client.chatMessage) < 256:
		splitLines(client.chatMessage, messageList, False, client)
		splitLines(messageList[1], messageList, True, client)
		splitLines(messageList[2], messageList, True, client)
		sendMessage(messageList, client)
					
	else:
		client.chatMessage = client.chatMessage[:255]	#cut the message off at 256 characters

		splitLines(client.chatMessage, messageList, False, client)
		splitLines(messageList[1], messageList, True, client)
		splitLines(messageList[2], messageList, True, client)
		sendMessage(messageList, client)
		
	#prepare to accept the next message from the user
	client.setMessageNotFinished(True)
	client.setChatMessage("")


def splitLines(message, messageList, hasBeenSplit, client):
	#split the message into two lines
	notSplit = True
	if hasBeenSplit == False:
		position = 64 - (len(client.user_name)+4)
		if position < 0:
			position = 0
	else:
		position = 64 + 4 #the extra 4 is for the tab, and user names cancel each other out.

	while notSplit == True:
		if message[position] == " ":
			messageA = message[:position]
			messageB = "    " + str(message[position:])
			if hasBeenSplit == False:
				messageList.append(messageA)
				messageList.append(messageB)
			else:
				messageList.pop()
				messageList.append(messageA)
				messageList.append(messageB)

			notSplit = False

		else:
			position -= 1
	return messageList


def sendMessage(messageList, client):
	firstMessage = messageList.pop(0)
	client.Message(firstMessage)
	for message in messageList:
		client.Message(message, True)


def keyProcessor(key_pressed, client):
	#run when each key is pressed.  Handles adding the keypress to the message, or sending the message to be formatted and displayed if enter is pressed
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

	# defines and replaces the symbols on the keyboard accessed with shift

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
	