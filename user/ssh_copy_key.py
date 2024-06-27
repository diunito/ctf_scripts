#!/bin/env python3
import os
import subprocess
import getpass

def create_ssh_key(name):
    key_path = os.path.expanduser(f"~/.ssh/{name}")
    if not os.path.exists(key_path):
        subprocess.run(['ssh-keygen', '-t', 'rsa', '-b', '2048', '-f', key_path, '-N', ''])
    else:
        print(f"Key {name} already exists.")
    return key_path

def add_to_ssh_config(name, ip_address):
    config_path = os.path.expanduser("~/.ssh/config")
    with open(config_path, 'a') as config_file:
        config_file.write(f"\nHost {name}\n")
        config_file.write(f"    HostName {ip_address}\n")
        config_file.write(f"    User {getpass.getuser()}\n")
        config_file.write(f"    IdentityFile ~/.ssh/{name}\n")
        config_file.write(f"    IdentitiesOnly yes\n")

def ssh_copy_id(name, ip_address, password):
    key_path = os.path.expanduser(f"~/.ssh/{name}.pub")
    ssh_copy_id_cmd = ['ssh-copy-id', '-i', key_path, f"{getpass.getuser()}@{ip_address}"]
    sshpass_cmd = ['sshpass', '-p', password]
    sshpass_cmd.extend(ssh_copy_id_cmd)
    subprocess.run(sshpass_cmd)

def main():
    name = input("Enter the name: ")
    ip_address = input("Enter the IP address: ")
    password = getpass.getpass("Enter the password: ")

    create_ssh_key(name)
    add_to_ssh_config(name, ip_address)
    ssh_copy_id(name, ip_address, password)

    print(f"SSH key generated, config updated, and key copied to {ip_address}.")

if __name__ == "__main__":
    main()
