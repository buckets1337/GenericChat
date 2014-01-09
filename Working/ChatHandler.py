#Chat &ler.py
# &les chat message functionality & formatting

import pygame
from os import environ

def formatMessage(client):
	messageList = []
	# Splits client.chatMessage into up to 4 lines based on length, & sends them as separate messages so they show up on separate lines
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
		position = 64 + 4 #the extra 4 is for the tab, & user names cancel each other out.

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
	#run when each key is pressed.   &les adding the keypress to the message, or sending the message to be formatted & displayed if enter is pressed
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
			if (key_pressed != pygame.K_CAPSLOCK and
				character != "f1" and
				character != "f2" and
				character != "f3" and
				character != "f4" and
				character != "f5" and
				character != "f6" and
				character != "f7" and
				character != "f8" and
				character != "f9" and
				character != "f10" and
				character != "f11" and
				character != "f12" and
				character != "left alt" and
				character != "right alt" and
				character != "left ctrl" and
				character != "right ctrl" and
				character != "left super" and
				character != "right super" and
				character != "menu" and
				character != "delete" and
				character != "insert" and
				character != "home" and
				character != "page up" and
				character != "page down" and
				character != "print screen" and
				character != "scroll lock" and
				character != "pause" and
				character != "tab" and
				character != "up" and
				character != "down" and
				character != "left" and
				character != "right" and
				character != "numlock" and
				character != "[/]" and
				character != "[*]" and
				character != "[-]" and
				character != "[+]" and
				character != "enter" and
				character != "[.]" and
				character != "[0]" and
				character != "[1]" and
				character != "[2]" and
				character != "[3]" and
				character != "[4]" and
				character != "[5]" and
				character != "[6]" and
				character != "[7]" and
				character != "[8]" and
				character != "[9]"			
				):
					#if len(client.chatMessage) < 64:
					message = client.chatMessage + character
					client.setChatMessage(message)


def shiftResolve(character):

	# defines & replaces the symbols on the keyboard accessed with shift

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
	