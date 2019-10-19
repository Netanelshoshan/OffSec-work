#!/bin/bash

# reset all counters and iptables rules
iptables -Z && iptables -F
# measure incoming traffic to x.x.x.x
iptables -I INPUT 1 -s 10.11.22.105 -j ACCEPT
# measure outgoing traffic to x.x.x.x
iptables -I OUTPUT 1 -d 10.11.22.105 -j ACCEPT
