#!/usr/bin/python

import socket
import sys

if len(sys.argv) != 2:
	print "Usage: vrfy.py <username>"
	sys.exit(0)

s = socket.socket(socket.AF_INET , socket.SOCK_STREAM) # Create a socket
connect = s.connect(('10.11.1.229' , 25 )) # Connect to the server
banner = s.recv(1024)
print banner
s.send ('VRFY' + sys.argv[1] + '\r\n')  # VRFY a user
result = s.recv(1024)
print result
s.close() 			       # Close the socket
