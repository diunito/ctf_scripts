#!/bin/bash 

# """
# file per automatizzare un po' di azioni allinizio della ctf, in ordine:
#
# 1. Download del proxy
# 2. Generazione della chiave ssh
# 5. Avvio del proxy
#"""


# check sudo 
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# install python3 and tmux
echo "Installing python3 and tmux"
apt install python3 tmux -y
# pacman -S python3 tmux --noconfirm
# dnf install -y python3 tmux 


#  start download the proxy file
echo "Downloading the proxy file"
curl https://raw.githubusercontent.com/Pwnzer0tt1/firegex/main/start.py -o firegex.py


# GENERAZIONE CHIAVE SSH DA SISTEMARE

ssh-keygen -t rsa -b 4096 -C "firegex" -f ~/.ssh/id_rsa -q -N ""
# save the public key in the local file
cat ~/.ssh/id_rsa.pub > ~/.ssh/authorized_keys


# choose proxy port

echo "Ports in use by other services"
sudo lsof -i -P -n | grep LISTEN

 echo "Choose a port for the proxy (default 4444):"
 read port
 if [ -z "$port" ]; then
     port=4444
 fi

# choose proxy password
 echo "Choose a password for the proxy (default unito_team):"
 read password
 if [ -z "$password" ]; then
     password=unito_team
 fi

# download tcp dumper
wxho "Download TCP Dumper"
wget https://raw.githubusercontent.com/AlessandroMIlani/ctf_scripts/main/dump.sh
chmod +x dump.sh

echo "Starting the proxy"
python3 firegex.py -p $port
