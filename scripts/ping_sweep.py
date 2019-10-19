#!/usr/bin/Python3

import ipaddress 
import os

ip_input = input("Please provide network IP:")
network = ipaddress.ip_network(ip_input)


for ip in network.hosts():
	os.system("ping {} -c1 | grep 'bytes from' | cut -d ' ' -f4 | cut -d ':' -f1 |sort -u |tee -a ping_sweep.txt &""".format(ip))
	
	
