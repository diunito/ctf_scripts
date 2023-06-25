#!/bin/bash

# check sudo
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

interrupt_handler() {
    echo "Interruzione ricevuta. Terminazione in corso..."
    # Puoi aggiungere eventuali azioni di pulizia o altre operazioni qui, se necessario.
    # Ad esempio, puoi terminare il processo tcpdump usando il suo PID (se disponibile).
    if [[ -n $tcpdump_pid ]]; then
        kill $tcpdump_pid
    fi
    exit 1
}

trap interrupt_handler SIGINT

# check args < 1
if [ $# -lt 1 ];
  then
    echo "No arguments supplied"
    echo "Usage: ./dump.sh <dir>" 
    echo "or"
    echo "Usage: ./dump.sh <dir> <tulip_ip> <tulip_password>"
    exit
fi

dir=$1

if [ $# -eq 3 ];
  then
    ip=$2
    pass=$3
fi

# check if dir exist
if [ ! -d "$dir" ]; then
    echo "Folder $dir does not exist"
    mkdir $1
fi


i=1
j=1
# check if exist files on format CTF_dump_*.pcap
if [ "$(ls -A $dir) | grep CTF_dump" ]; then
    i=$(ls -A $dir | grep CTF_dump | tail -n 1 | cut -d'_' -f3 | cut -d'.' -f1)
    echo "Last dump file: $i"
    i=$((i+1))
    echo "Continue from $i"
fi

# start dump and upload 
while true
do
    echo "Dumping $i"
    timeout 120 tcpdump -i game -w ${dir}CTF_dump_$i.pcap port not 22 &
    tcpdump_pid=$!
    wait $tcpdump_pid
    if [ $# -eq 3 ];
      then
        echo "Uploading $i"
        curl -F "file=@${dir}CTF_dump_$i.pcap" http://$ip:5000/upload -u "tulip:$pass"
    fi
    i=$((i+1))
    sleep 2
done
