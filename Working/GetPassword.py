#GetPassword.py
#Handles login password-related stuff


import getpass




def send(username, connection):
	# gets a password, and sends it to the server

	client_password = str(getpass.getpass())
	user_name = str(username)

	connection.Send({"action":"CheckPassword", "user_name":user_name, "password":client_password})


def checkUsernameExists(username, connection):
	user_name = str(username)

	connection.Send({"action":"CheckUsernameExists", "user_name":user_name})


def new(client):
				# new user!
	client.Send({"action":"NewUser"})
