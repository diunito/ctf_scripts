#!/bin/bash 

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


echo "Downloading the proxy"
git clone https://github.com/ByteLeMani/ctf_proxy


# download tcp dumper
wxho "Download TCP Dumper"
wget https://raw.githubusercontent.com/AlessandroMIlani/ctf_scripts/main/dump.sh
chmod +x dump.sh


