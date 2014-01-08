# ClientRenderer.py
# Renders the client's screen
import CONFIG

import pygame

pygame.init()

chatFont = pygame.font.Font(None, CONFIG.DEFAULT_FONT_SIZE)

ChatWindow = pygame.Surface((CONFIG.CHAT_WINDOW_WIDTH, CONFIG.CHAT_WINDOW_HEIGHT))


def RenderChat(screen, client):		#Renders the chat window

	currentMessageBuffer = client.chatMessage
	chatLine = chatFont.render(">> " + str(currentMessageBuffer), 1, CONFIG.COLOR_WHITE)

	#print client.chatBuffer
	#ChatLogScreen = spawnChatBuffer(client.chatBuffer)

	ChatWindow.fill(CONFIG.COLOR_BLUE)
	ChatWindow.blit(chatLine, (3, (CONFIG.CHAT_WINDOW_HEIGHT - CONFIG.DEFAULT_FONT_SIZE + 2)))
	#ChatWindow.blit(ChatLogScreen, (3, (CONFIG.SCREEN_HEIGHT - CONFIG.CHAT_WINDOW_HEIGHT)))

	screen.blit(ChatWindow, (3, CONFIG.SCREEN_HEIGHT  - (CONFIG.CHAT_WINDOW_HEIGHT + 3)))


def spawnChatBuffer(chatBuffer):
	#print chatBuffer
	
	numBufferItems = len(chatBuffer)
	#print numBufferItems
	ChatLogScreen = pygame.Surface((CONFIG.CHAT_WINDOW_WIDTH, CONFIG.CHAT_WINDOW_HEIGHT - (CONFIG.DEFAULT_FONT_SIZE) - 2))

	for i in range(0, numBufferItems):
		#print i
		
		lineItem = chatBuffer[-i]
		bufferLine = chatFont.render(lineItem, 1, CONFIG.COLOR_WHITE)
		ChatLogScreen.blit(bufferLine, (3, (CONFIG.CHAT_WINDOW_HEIGHT - ((i * CONFIG.DEFAULT_FONT_SIZE)+ CONFIG.DEFAULT_FONT_SIZE))))
	#print "Chat log:" + str(ChatLogScreen)
	return ChatLogScreen


def spawnLargeChatBuffer(chatBuffer):
	#print chatBuffer
	
	numBufferItems = len(chatBuffer)
	#print numBufferItems
	ChatLogScreen = pygame.Surface((CONFIG.CHAT_WINDOW_WIDTH, CONFIG.CHAT_WINDOW_LARGE_HEIGHT - (CONFIG.DEFAULT_FONT_SIZE) - 2))

	for i in range(0, numBufferItems):
		#print i
		
		lineItem = chatBuffer[-i]
		bufferLine = chatFont.render(lineItem, 1, CONFIG.COLOR_WHITE)
		ChatLogScreen.blit(bufferLine, (3, (CONFIG.CHAT_WINDOW_LARGE_HEIGHT - ((i * CONFIG.DEFAULT_FONT_SIZE)+ CONFIG.DEFAULT_FONT_SIZE))))
	#print "Chat log:" + str(ChatLogScreen)
	return ChatLogScreen


def RenderChatBuffer(screen, client, location):
	ChatLogScreen = spawnChatBuffer(client.chatBuffer)

	screen.blit(ChatLogScreen, (location[0],location [1]))


def RenderLargeChatBuffer(screen, client, location):
	ChatLogScreen = spawnLargeChatBuffer(client.chatBuffer)

	screen.blit(ChatLogScreen, (location[0],location [1]))


def RenderAll(screen, client):		# Renders everything
	screen.fill(CONFIG.COLOR_BLACK)

	if client.state == "Chat":
		RenderChat(screen, client)
		RenderLargeChatBuffer(screen, client, (3, CONFIG.SCREEN_HEIGHT  - (CONFIG.CHAT_WINDOW_LARGE_HEIGHT + 3)) )

	if client.state == "Normal":
		RenderChatBuffer(screen, client, (3, CONFIG.SCREEN_HEIGHT  - (CONFIG.CHAT_WINDOW_HEIGHT + 3 - CONFIG.DEFAULT_FONT_SIZE)))

	pygame.display.update()