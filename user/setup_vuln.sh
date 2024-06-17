#!/bin/bash

[ -z "$1" ] && echo "need ip as first arg" && exit 1

ip="$1"
user="${2:-root}"
port="${3:-22}"
ssh_folder_path="../../priv/.ssh"
key_name="vulnbox"
home_folder=$(ssh "${user}@${ip}" 'echo $HOME')

ssh -p $port "${user}@${ip}" 'mkdir -p $HOME/.ssh'

rsync -Pav --rsh="ssh -p $port" "${ssh_folder_path}/${key_name}" "${ssh_folder_path}/${key_name}" "${ip}:$h$user/.ssh"

ssh_conf="Host github.com
  IdentityFile '~/.ssh/${key_name}'
  User git"
echo "$ssh_conf" | ssh -p $port "${user}@${ip}" 'cat - >> \$HOME/.ssh/config'

ssh -p $port "${user}@${ip}" 'cd $HOME;sh <(curl -sL https://raw.githubusercontent.com/koraynilay/simad/main/deploy_clone.sh);./deploy_clone.sh'
