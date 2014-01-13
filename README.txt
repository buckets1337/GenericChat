This is an attempt to wrap my head around networking using Python
and the PodSixNet library.  

Requires Python 2.7, pygame, and passlib

What is working:
	-A generic chat program that works over a network. There
	are both client and server scripts, and any number of clients
	can connect to one server

	-Logging for both the server and the client.  However, it
	does appear that opening a log while the program is running
	breaks the log...and it appears to do so for the rest of the
	calendar day

	-Output is visible in both the console and the GUI

What is not working:
	-I seem to have misplaced the work I did on giving everyone
	an avatar and means to control it.  Re-implementing this
	will probably be next


Anyway, basic controls.

` or ~ (same key) opens the chat window
Just type messages and hit enter.
arrow key left or right moves the cursor
arrow key up or down scrolls through chat history
esc closes the chat window, but does not end the session
break (ctrl-c) in the console or press the end key in game to exit
f8 toggles fullscreen
prtscn to take a screenshot


To run the program:
Launch an instance of the server, using the syntax provided if you screw it up. (start with python GenericServer.py)

Launch 2 or more instances of the client, using the syntax it provides.

Chat with yourself!  Or if you're lucky enough to have friends willing to demo
an underdeveloped program, chat with them!

Both server and client logs are found in the "log" directory

the passwordHash file in the serverData directory contains all the passwords.  If you're getting immediate disconnects by clients on connection, try deleting this file.
Everyone will have to re-enter their passwords the next time they log in, but it should help clear up issues related to corrupted hashes in this file.
