#!/bin/bash

for ip in $(seq 1 255); do
host -t ns 10.11.1.$ip |column -t

done
