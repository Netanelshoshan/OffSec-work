#!/bin/python

print "[-] Initial fuzz crashed the server at 2900 bytes."
print ""
print "[-] I used the MSF pattern_create to create a random bytes and send it again,\n\tthis time the EIP reg was pointing to 39694438."
print ""
print "[-] After that, I used the pattern_offset to calculate the exact byte that crashes the server" 

