#!/bin/bash

# get the tulip folder

#read -p "Insert the tulip folder path: " path
path="/home/ale/CTF/tool/tulip/pcaps"

#read -p "Insert vuln ip: " ip
ip="10.60.41.1"

#read -p "Insert vuln passwd: " REPLY
REPLY="AeM0i4ZNtLljgIXp"

# evry 2 minutes download folder from vuln
while true; do
    sshpass -p $REPLY scp -r root@$ip:/tmp/pcap $path
    sleep 120
done
