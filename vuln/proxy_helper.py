import docker
import json
import requests
import os
import glob

import logging

def get_container_info():
    names = {}
    client = docker.from_env()
    containers = client.containers.list()
    for container in containers:
        ports = container.ports
        name = container.name
        if ports:
            for port in ports:
                # Stampa il nome del container e la porta mappata sull'host
                # print("[+] Container: " + name + " Port: " + port)
                logging.info("[+] Container: " + name + " Port: " + port)
                # dictionary name, port list
                if name not in names:
                    names[name] = []
                    names[name].append(port[:-4])
                else:
                    names[name].append(port[:-4])
    return names

def create_json(containers):
    services = []
    for container in containers:
        service = {
            "name": container,
            "target_ip": container,
            "target_port": int(containers[container][0]) + 1,
            "listen_port": int(containers[container][0])
        }            
        # if localhost:port retrun an http response add http = True
        try:
            r = requests.get('http://localhost:' + str(containers[container][0]))
            logging.info('[+] http://localhost:' + str(containers[container][0]) + ' status code:' + str(r.status_code))
            if r.status_code == 200:
                service['http'] = True
        except:
            service['http'] = False
        services.append(service)
    
    glbal_conf = {
        "keyword": "EH! VOLEVI",
        "verbose": False,
        "dos": {
            "enabled": False,
            "duration": 60,
            "interval": 2
        },
        "max_stored_messages": 10,
        "max_message_size": 65535
    }
    
    data = {
        "services": services,
        "global_config": glbal_conf
    } 

    return data  

def compose_backup(compose_files):
    # create file docker-compose.yml.bak for each docker-compose.yml on same folder
    for compose_file in compose_files:
        with open(compose_file, 'r') as file:
            lines = file.readlines()
            with open(compose_file + '.bak', 'w') as file2:
                file2.writelines(lines)
    # print('[+] Backup created')
    logging.info('[+] Created backup for docker-compose.yml files')

def edit_compose(main_folder, containers):
    logging.info('[+] Start editing docker-compose.yml files')
    compose_files = glob.glob(os.path.join(main_folder, '**/docker-compose.yml'), recursive=True) + \
               glob.glob(os.path.join(main_folder, '**/docker-compose.yaml'), recursive=True)
    compose_files = [x for x in compose_files if 'ctf_proxy' not in x]
    
    compose_backup(compose_files)
    
    text_to_add = '''

networks:
  default:
    name: ctf_network
    external: true'''

    for compose_file in compose_files:
        with open(compose_file, 'a') as file:
            file.write(text_to_add)

    for conteiner in containers:
        #search containers[conteiner][0] in compose_files
        for compose_file in compose_files:
            with open(compose_file, 'r') as file:
                lines = file.readlines()
                for i in range(len(lines)):
                    if containers[conteiner][0] in lines[i]:
                        port = int(containers[conteiner][0]) + 1
                        # copy line until -
                        space = lines[i].split('-')[0]
                        old_line = lines[i]
                        lines[i] = space + '- "' + str(port) +'"'+ '\n'
                        with open(compose_file, 'w') as file2:
                            file2.writelines(lines)
                            # print folder name, old line and new line
                            # print('[+] ' + 'Container: ' + conteiner + '\n[+] Old line: ' + lines[i] + '\n[+] New line: ' + lines[i].strip())
                            logging.info('[+] ' + 'Container: ' + conteiner + ' Old line: ' + old_line.strip() + ' New line: ' + lines[i].strip())
                        break  
                
    return 0

if __name__ == "__main__":
    
    # start logging namee file logfile+timestamp
    logging.basicConfig(level=logging.INFO, filename="proxy_helper.logs", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info("Start logging")
    
    # get container
    containers = get_container_info() 
    
    # create data strcture
    data = create_json(containers)
    json_data = json.dumps(data, indent=4)
    
    # write data on config.json
    with open('./ctf_proxy/proxy/config/config.json', 'w') as outfile:
        outfile.write(json_data)
    logging.info('[+] Updated config.json file with new containers')
        
    # edit docker-compose.yml files
    main_folder = os.getcwd()
    res = edit_compose(main_folder, containers)
