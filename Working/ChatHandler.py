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
		

	elif len(client.chatMessage) < (192 - (len(client.user_name) + 4)):
		splitLines(client.chatMessage, messageList, False, client)
		splitLines(messageList[1], messageList, True, client)
		sendMessage(messageList, client)

	elif len(client.chatMessage) < (256 - (len(client.user_name) + 4)):
		splitLines(client.chatMessage, messageList, False, client)
		splitLines(messageList[1], messageList, True, client)
		splitLines(messageList[2], messageList, True, client)
		sendMessage(messageList, client)

					
	else:
		client.chatMessage = client.chatMessage[:256]	#cut the message off at 256 characters

		splitLines(client.chatMessage, messageList, False, client)
		splitLines(messageList[1], messageList, True, client)
		splitLines(messageList[2], messageList, True, client)
		splitLines(messageList[3], messageList, True, client)
		sendMessage(messageList, client)
		
	#prepare to accept the next message from the user
	client.setMessageNotFinished(True)
	client.setChatMessage("")


def splitLines(message, messageList, hasBeenSplit, client):
	#split the message into two lines

	notSplit = True
	originalPosition = 0

	if hasBeenSplit == False:
		position = 64 - (len(client.user_name)+4)
		if position < 0:
			position = 0
		if position > 64:
			position = 64
		if position > len(message):
			position = len(message)

		originalPosition = int(position)
	else:
		position = 64 + 4 #the extra 4 is for the tab, & user names cancel each other out.
		if position > len(message):
			position = len(message)
		if position < 0:
			position = 0

		originalPosition = int(position)			

	while notSplit == True:

		def appendMessages(messageA, messageB):
			if hasBeenSplit == False:
				messageList.append(messageA)
				messageList.append(messageB)
			else:
				messageList.pop()
				messageList.append(messageA)
				messageList.append(messageB)

		if message[position] == " ":
			messageA = message[:position]
			messageB = "    " + str(message[position:])
			appendMessages(messageA, messageB)

			notSplit = False

		else:
			if position > 0:
				position -= 1
			elif position == 0:
				pass

				messageA = message[:originalPosition]
				messageB = "    " + str(message[originalPosition:])
				appendMessages(messageA, messageB)

	return messageList


def sendMessage(messageList, client):
	firstMessage = messageList.pop(0)
	client.Message(firstMessage)
	for message in messageList:
		client.Message(message, True)


def keyProcessor(key_pressed, client):
	#run when each key is pressed.   handles adding the keypress to the message, or sending the message to be formatted & displayed if enter is pressed
	character = pygame.key.name(key_pressed)

	client.chatMessage = client.chatMessage[:(client.chatCursorLocation)] + client.chatMessage[(client.chatCursorLocation + 1):]

	#print client.chatCursorLocation

	if client.CapsLock == True:
		character = character.upper()

	if key_pressed == pygame.K_LSHIFT or key_pressed == pygame.K_RSHIFT or character == "left shift" or character == "right shift" or character == "LEFT SHIFT" or character == "RIGHT SHIFT":		
		client.setIsCapital(True)
		#print client.isCapital

	if character == "caps lock" or character == "CAPS LOCK":

		if client.CapsLock == True:
			message = client.chatMessage[:(client.chatCursorLocation)] + "|" + client.chatMessage[client.chatCursorLocation:]
		else:
			message = client.chatMessage
		client.setCapsLock(True)
		client.setChatMessage(message)
		#print "CapsLock on"

	if (character == "`" or 
		character == "escape" or
		character == "left shift" or 
		character == "right shift" or
		character == "LEFT SHIFT" or
		character == "RIGHT SHIFT" or
		character == "left ctrl" or
		character == "right ctrl" or
		character == "left alt" or
		character == "right alt" or
		character == "caps lock" or
		character == "CAPS LOCK"):
	 		character = ""

	if key_pressed == pygame.K_RETURN:
		client.setMessageNotFinished(False)
		client.chatCharacterCounter = 0
		client.chatCursorLocation = 0
		client.overbuffer = False
		

	elif key_pressed == pygame.K_SPACE:
		#if len(client.chatMessage) < 64:
		message = client.chatMessage[:client.chatCursorLocation] + " |" + client.chatMessage[client.chatCursorLocation:]

		client.setChatMessage(message)
		client.chatCharacterCounter += 1
		client.chatCursorLocation += 1
		client.overbuffer = False
		#print client.chatCursorLocation

	elif key_pressed == pygame.K_BACKSPACE:
		if client.chatMessage != "":
			message = client.chatMessage[:(client.chatCursorLocation - 1)] + "|" + client.chatMessage[client.chatCursorLocation:]
			client.setChatMessage(message)
			client.chatCharacterCounter -= 1
			client.chatCursorLocation -= 1
			client.overbuffer = False
			#print client.chatCursorLocation

	elif key_pressed == pygame.K_LEFT:
		client.chatCursorLocation -= 1
		if client.chatCursorLocation < 0:
			client.chatCursorLocation = 0
		message = client.chatMessage[:client.chatCursorLocation] + "|" + client.chatMessage[client.chatCursorLocation:]
		client.setChatMessage(message)
		#print client.chatCursorLocation

	elif key_pressed == pygame.K_RIGHT:
		client.chatCursorLocation += 1
		if client.chatCursorLocation > len(client.chatMessage):
			client.chatCursorLocation = len(client.chatMessage)
		message = client.chatMessage[:client.chatCursorLocation] + "|" + client.chatMessage[client.chatCursorLocation:]
		client.setChatMessage(message)
		#print client.chatCursorLocation

	elif key_pressed == pygame.K_UP:
		if client.chatHistoryCounter > 0:
			client.chatHistoryCounter -=1
			#print "History:" + str(client.chatHistoryCounter) + "History List:" + str(len(client.chatHistoryList))
			if client.chatHistoryCounter < 0:
				client.chatHistoryCounter = 0
			client.chatMessage = client.chatHistoryList[client.chatHistoryCounter] + "|" 
		else:
			client.chatMessage = client.chatMessage + "|"
		client.chatCursorLocation = len(client.chatMessage) - 1
			

	elif key_pressed == pygame.K_DOWN:
		if client.chatHistoryCounter < len(client.chatHistoryList):
			
			client.chatMessage = client.chatHistoryList[client.chatHistoryCounter]
			if client.chatHistoryCounter < len(client.chatHistoryList) - 1:
				client.chatHistoryCounter += 1
			#print "History:" + str(client.chatHistoryCounter) + "History List:" + str(len(client.chatHistoryList))
			if client.chatHistoryCounter > 31:
				client.chatHistoryCounter = 31
			client.chatMessage = client.chatHistoryList[client.chatHistoryCounter] + "|"
		else:
			client.chatMessage = client.chatMessage + "|"
		client.chatCursorLocation = len(client.chatMessage) - 1

	else:
		if character != "":
			#print client.isCapital
			#print character
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
				character != "`" and
				character != "escape" and
				character != "left alt" and
				character != "right alt" and
				character != "left shift" and
				character != "right shift" and
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

					messageWordList = client.chatMessage.split(" ")
					if len(messageWordList[-1]) >= 32:
						client.overbuffer = True

					if ((client.chatCharacterCounter >= 32 and " " not in client.chatMessage) or 
						(len(client.chatMessage) > 256) or 
						(client.overbuffer == True)):
							message = client.chatMessage[:(client.chatCursorLocation)] + "|" + client.chatMessage[(client.chatCursorLocation):]
							#print client.chatCursorLocation
					else:
						message = client.chatMessage[:(client.chatCursorLocation)] + character + "|" + client.chatMessage[(client.chatCursorLocation):]
						client.chatCharacterCounter += 1
						client.chatCursorLocation += 1
						#print client.chatCursorLocation
			
					client.setChatMessage(message)
			else:
				message = client.chatMessage[:(client.chatCursorLocation)] + "|" + client.chatMessage[(client.chatCursorLocation):]
				client.setChatMessage(message)

		if character == "":
			message = client.chatMessage[:(client.chatCursorLocation)] + "|" + client.chatMessage[(client.chatCursorLocation):]
			client.setChatMessage(message)


def shiftResolve(character):

	# defines & replaces the symbols on the keyboard accessed with shift

	#print character

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
	
	#print "shiftResolve"
	return character
	