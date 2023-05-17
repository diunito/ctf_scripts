#!/bin/bash 

# """
# file per automatizzare un po' di azioni allinizio della ctf, in ordine:
#
# 1. Download del proxy
# 2. Generazione della chiave ssh
# 5. Avvio del proxy
#"""

# install python3 and tmux
echo "Installing python3 and tmux"
sudo apt install python3 tmux -y

#  start download the proxy file
echo "Downloading the proxy file"
curl https://raw.githubusercontent.com/Pwnzer0tt1/firegex/main/start.py -o firegex.py


# GENERAZIONE CHIAVE SSH DA SISTEMARE

ssh-keygen -t rsa -b 4096 -C "firegex" -f ~/.ssh/id_rsa -q -N ""
# save the public key in the local file
cat ~/.ssh/id_rsa.pub > ~/.ssh/authorized_keys


# choose proxy port
 echo "Choose a port for the proxy (default 4444):"
 read port
 if [ -z "$port" ]; then
     port=4444
 fi

# choose proxy password
 echo "Choose a password for the proxy (default firegex):"
 read password
 if [ -z "$password" ]; then
     password=firegex
 fi


echo "Starting the proxy"
python3 firegex.py -p $port -P $password
