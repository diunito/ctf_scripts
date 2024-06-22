#!/bin/bash

[ -z "$1" ] && echo "need ip as first arg" && exit 1
ssh -G '*' | grep 'controlmaster false' && echo "you should probably enable a ControlMaster in your ssh config"

ip="$1"
user="${2:-root}"
port="${3:-22}"
ssh_folder_path="$HOME/.ssh"
key_name="vulnbox"

sp='sshpass -eSSHPASS'
export SSHPASS=$(<../../priv/.vm-pass)

home_folder=$($sp ssh -p $port "${user}@${ip}" 'echo $HOME')

$sp ssh -p $port "${user}@${ip}" 'mkdir -vp $HOME/.ssh'

$sp rsync -Pav --rsh="ssh -p $port" "${ssh_folder_path}/${key_name}" "${ssh_folder_path}/${key_name}.pub" "${user}@${ip}:${home_folder}/.ssh"

ssh_conf="Host github.com
  IdentityFile ~/.ssh/${key_name}
  User git"
echo "$ssh_conf" | $sp ssh -p $port "${user}@${ip}" 'cat - >> $HOME/.ssh/config; cat $HOME/.ssh/config'

$sp ssh -p $port "${user}@${ip}" 'ssh-keyscan github.com >> $HOME/.ssh/known_hosts; cd $HOME;curl -sL https://raw.githubusercontent.com/koraynilay/simad/main/deploy_clone.sh -o deploy_clone.sh; chmod +x deploy_clone.sh'
