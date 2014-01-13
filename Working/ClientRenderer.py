# ClientRenderer.py
# Renders the client's screen

import CONFIG

import pygame

pygame.init()

chatFont = pygame.font.Font(None, CONFIG.DEFAULT_FONT_SIZE)

ChatWindow = pygame.Surface((CONFIG.CHAT_WINDOW_WIDTH, CONFIG.CHAT_WINDOW_HEIGHT))


def RenderChat(screen, client):		#Renders the chat input window

	if screen != "":
		currentMessageBuffer = client.chatMessage
		if len(currentMessageBuffer) > 66:
			currentMessageBuffer = currentMessageBuffer[-66:]
		chatLine = chatFont.render(">> " + str(currentMessageBuffer), 1, CONFIG.COLOR_WHITE)

		#print client.chatBuffer
		#ChatLogScreen = spawnChatBuffer(client.chatBuffer)

		ChatWindow.fill(CONFIG.COLOR_BLUE)
		ChatWindow.blit(chatLine, (3, (CONFIG.CHAT_WINDOW_HEIGHT - CONFIG.DEFAULT_FONT_SIZE + 2)))
		#ChatWindow.blit(ChatLogScreen, (3, (CONFIG.SCREEN_HEIGHT - CONFIG.CHAT_WINDOW_HEIGHT)))

		screen.blit(ChatWindow, (3, CONFIG.SCREEN_HEIGHT  - (CONFIG.CHAT_WINDOW_HEIGHT + 3)))


def spawnChatBuffer(chatBuffer, size):
	#print chatBuffer
	
	numBufferItems = len(chatBuffer)
	#print numBufferItems
	if size == "normal":
		ChatLogScreen = pygame.Surface((CONFIG.CHAT_WINDOW_WIDTH, CONFIG.CHAT_WINDOW_HEIGHT - (CONFIG.DEFAULT_FONT_SIZE) - 2))
	if size == "large":
		ChatLogScreen = pygame.Surface((CONFIG.CHAT_WINDOW_WIDTH, CONFIG.CHAT_WINDOW_LARGE_HEIGHT - (CONFIG.DEFAULT_FONT_SIZE) - 2))

	for i in range(0, numBufferItems):
		#print i
		
		lineItem = chatBuffer[-i]
		bufferLine = chatFont.render(lineItem, 1, CONFIG.COLOR_WHITE)
		if size == "normal":
			ChatLogScreen.blit(bufferLine, (3, (CONFIG.CHAT_WINDOW_HEIGHT - ((i * CONFIG.DEFAULT_FONT_SIZE)+ CONFIG.DEFAULT_FONT_SIZE))))
		if size == "large":
			ChatLogScreen.blit(bufferLine, (3, (CONFIG.CHAT_WINDOW_LARGE_HEIGHT - ((i * CONFIG.DEFAULT_FONT_SIZE)+ CONFIG.DEFAULT_FONT_SIZE))))
	#print "Chat log:" + str(ChatLogScreen)
	return ChatLogScreen


def RenderChatBuffer(screen, client, location, size):
	# renders a log of all messages above the chat input window
	if screen != "":
		if size == "normal":
			ChatLogScreen = spawnChatBuffer(client.chatBuffer, "normal")

			screen.blit(ChatLogScreen, (location[0],location [1]))

		if size == "large":
			ChatLogScreen = spawnChatBuffer(client.chatBuffer, "large")

			screen.blit(ChatLogScreen, (location[0],location [1]))


def RenderAll(screen, client):		# Renders everything
	if screen != "":
		screen.fill(CONFIG.COLOR_BLACK)

	if client.state == "Chat":
		RenderChat(screen, client)
		RenderChatBuffer(screen, client, (3, CONFIG.SCREEN_HEIGHT  - (CONFIG.CHAT_WINDOW_LARGE_HEIGHT + 3)), "large" )

	if client.state == "Normal":
		RenderChatBuffer(screen, client, (3, CONFIG.SCREEN_HEIGHT  - (CONFIG.CHAT_WINDOW_HEIGHT + 3 - CONFIG.DEFAULT_FONT_SIZE)), "normal")

	pygame.display.update()