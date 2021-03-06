#!/usr/bin/python3
##############################################################################################
# Program: 
#	chatserve.py 
# Author: 
#	Travis Laxson
# Description: 
# 	This python program serves as the chat server component for the TCP chat application. 
#	The program will listen for incoming chat client requests at the port specified in
# 	a command-line argument. Once a connection with client has been established, the chat 
# 	server will exchange messages with the chat client using a server screen name input 
# 	by the user. The server will close the TCP chat session with the command "\quit".
# Sources:
#	1) OSU - CS372 Lecture #15 slides 7-9
#	2) Executing proper command format - https://www.linode.com/docs/tools-reference/tools/modify-file-permissions-with-chmod/
#	3) I/O refresher - https://www.hackerearth.com/practice/python/getting-started/input-and-output/tutorial/
#	4) Encode server message - https://stackoverflow.com/questions/33054527/typeerror-a-bytes-like-object-is-required-not-str-when-writing-to-a-file-in
#	5) Python 3.6 Socket Programming Docs - https://docs.python.org/3.6/library/socket.html
# 	6) Python I/O help docs - https://pynative.com/python-input-function-get-user-input/
# 	7) Run python program from terminal in desired format - https://osu-cs.slack.com/archives/C0J3LH509/p1556883207107600
# Created: 
#	30 April 2019
# Last Modified:
#	05 May 2019 
# Course:
#	CS372 - Introduction to Networking
# Source code:
#	https://github.com/tlaxson14/TCPChat/blob/master/chatserve.py
##############################################################################################
import socket
import sys

# Error check for number of command line args
if len(sys.argv) != 2:
	sys.exit("ERROR: Invalid commands") 

serverSocket = socket.socket()

# Get the command line server port number
serverPort = int(sys.argv[1])

# Create TCP socket 
serverSocket.bind(("", serverPort))
serverSocket.listen(1)

# Get server screenname
serverName = input("Enter screen name: ")
serverHandle = serverName + "> "
print("Server name:", serverName)

# Display confirmation msg that socket and port available
print("Server running on port", serverPort)

# Run loop to wait for client requests
while True:
	connectionSocket, addre = serverSocket.accept()
	
	# Get initial client request message
	clientMsg = connectionSocket.recv(500)

	# Print byte-decoded client request
	print(clientMsg.decode())
	
	# Initialize and send initial server response once connection established  
	serverMsg = "-- Welcome to the TCP Chat Server! --" 
	connectionSocket.send(serverMsg.encode())
	
	# Receive client message
	while clientMsg != "\quit" and serverMsg != "\quit":
		clientMsg = connectionSocket.recv(500)
		print(clientMsg.decode())
		clientHandle = clientMsg.decode().split()[0]
		clientAction = str(clientMsg.decode().split()[1])
		#print(clientMsg,"\n",clientHandle,"\n",clientAction,"\n")

		
		# Check if client enters termination message to end connection to server	
		if clientAction == "\\quit":
			print("Client has disconnected")
			connectionSocket.close()
			break
		
		# Get server response message
		serverMsg = input(str(serverHandle))
		respMsg = str(serverHandle + serverMsg)	
	
		# Check if server response message is to end connection 
		if serverMsg == "\\quit":
			# Send final disconnect message to client before closing socket
			serverTerminate = "Disconnected from server"
			connectionSocket.send(serverTerminate.encode())
			connectionSocket.close()
			break
		
		# Send server response
		connectionSocket.send(respMsg.encode())

