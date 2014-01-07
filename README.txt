This is an attempt to wrap my head around networking using Python
and the PodSixNet library.  

What is working:
	-A generic chat program that works over a network. There
	are both client and server scripts, and any number of clients
	can connect to one server

	-Logging for both the server and the client.  However, it
	does appear that opening a log while the program is running
	breaks the log...and it appears to do so for the rest of the
	calendar day

	-Input is displayed while typing, however, it does not scroll
	with long messages

	-Output is visible in both the console and the GUI

What is not working:
	-I seem to have misplaced the work I did on giving everyone
	an avatar and means to control it.  Re-implementing this
	will probably be next

	-There is no cursor, and it does not scroll with long messages

	-Message lengths greater than 128 characters probably break
	the program currently.

	-My complete lack of documentation on this one.  Shame on me.


Anyway, basic controls.

` or ~ (same key) opens the chat window
Just type messages and hit enter.
esc closes the chat window, but does not end the session
break (ctrl-c) to exit


To run the program:
Launch an instance of the server, using the syntax provided if you screw it up.

Launch 2 or more instances of the client, using the syntax it provides.

Chat with yourself!  Or if you're lucky enough to have friends willing to demo
an underdeveloped program, chat with them!


So far, this has been testing using only localhost on one machine, so it is very
possible that there are bugs that will only rear their heads when run across the
network.  You have been warned.
