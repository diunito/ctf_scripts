#!/bin/bash

# get the tulip folder

if [ $# -ne 3 ];
  then
    echo "No arguments supplied"
    echo "Usage: ./tulip_companion.sh <vuln_box_ip> <vuln_box_password> <tulip_pcap_folder_path>"

ip=$1
PSWD=$2
path=$3

# evry 2 minutes download folder from vuln
while true; do
    sshpass -p $PSWD rsync -r root@$ip:/tmp/pcap/\* $path
    sleep 120
done
