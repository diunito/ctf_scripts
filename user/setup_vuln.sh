#!/bin/bash
ssh -G '*' | grep 'controlmaster false' && echo "you should probably enable a ControlMaster in your ssh config"

set -a
DOTPATH="../../priv"
. ../../priv/sh_env
set +a

ip="$VM_IP"
user="${VM_USER:-root}"
port="${VM_PORT:-22}"
ssh_folder_path="$HOME/.ssh"
key_name="vulnbox"

sp='sshpass -eVM_PASS'

home_folder=$($sp ssh -p "$port" "${user}@${ip}" 'echo $HOME')
if [ "$?" -ne 0 ];then
	exit 1
fi

$sp ssh -p "$port" "${user}@${ip}" 'mkdir -vp $HOME/.ssh'

$sp rsync -Pav --rsh="ssh -p $port" "${ssh_folder_path}/${key_name}" "${ssh_folder_path}/${key_name}.pub" "${user}@${ip}:${home_folder}/.ssh"

ssh_conf="Host github.com
  IdentityFile ~/.ssh/${key_name}
  User git"
echo "$ssh_conf" | $sp ssh -p $port "${user}@${ip}" 'cat - >> $HOME/.ssh/config; cat $HOME/.ssh/config'

$sp ssh -p "$port" "${user}@${ip}" 'echo alias gserve="''\"git init; git add -A; git -c user.name=teamunito -c user.email=vulnbox@teamunito.ccit commit -m first\"" >> $HOME/.bash_profile'

#$sp ssh -p "$port" "${user}@${ip}" 'cd $HOME; source .bash_profile; for folder in *; do cd "$folder"; gserve; cd ..; done'
$sp ssh -p "$port" "${user}@${ip}"

$sp ssh -p "$port" "${user}@${ip}" 'ssh-keyscan github.com >> $HOME/.ssh/known_hosts; cd $HOME;curl -sL https://raw.githubusercontent.com/koraynilay/simad/main/deploy_clone.sh -o deploy_clone.sh; chmod +x deploy_clone.sh; ./deploy_clone.sh; tmux ls'

$sp ssh-copy-id -p "$port" "${user}@${ip}" -i "${ssh_folder_path}/${key_name}"
