import docker
import json
import requests
import os
import glob
import logging
import yaml

# global array with services json
services = []
logging.basicConfig(level=logging.INFO, filename="proxy_helper.logs", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")


def compose_backup(compose_file):
    # create file docker-compose.yml.bak for each docker-compose.yml on same folder
    with open(compose_file, 'r') as file:
        lines = file.readlines()
        with open(compose_file + '.bak', 'w') as file2:
            file2.writelines(lines)
    logging.info('[+] Created backup for docker-compose.yml file')


def create_service(dock, ports):
    i = 0
    for port in ports:
        print("using port: " + port)
        service = {
                "name": dock + '_' + str(i),
                "target_ip": dock,
                "target_port": int(port) + 1,
                "listen_port": int(port)
            }
        i+=1
        try:
            r = requests.get('http://localhost:' + str(port))
            logging.info('[+] http://localhost:' + str(port) + ' status code:' + str(r.status_code))
            if r.status_code == 200:
                service['http'] = True
        except Exception as e:
            logging.error(e)
            service['http'] = False
        print(service)
        services.append(service)
        print(services)
        logging.info('[+] Added service: ' + dock + " - port: " + port + ' to config.json') 
    pass
   
   
def add_network(file): 
    text_to_add = '''

networks:
  default:
    name: ctf_network
    external: true'''
    
    with open(file, 'a') as file:
        file.write(text_to_add)
    
def get_docker_services(folders):
    pass
    for folder in folders:
        # if docker-compose.yaml exists rename it to docker-compose.yml
        if os.path.isfile(folder + '/docker-compose.yaml'):
            os.rename(folder + '/docker-compose.yaml', folder + '/docker-compose.yml')
            logging.info('[+] Renamed docker-compose.yaml to docker-compose.yml in folder: ' + folder)
                    
        # open docker-compose.yml file
        with open(folder + '/docker-compose.yml', 'r') as file:
            docker_config = yaml.load(file, Loader=yaml.FullLoader)
            # get all services names
            services_names = docker_config['services'].keys()
            # convert to list 
            services_names = list(services_names)
            # get all ports for each service
            for service in services_names:
                # get ports
                try:
                    ports = docker_config['services'][service]['ports']
                    clean_ports = []
                    for i in range(len(ports)):
                        if len(ports[i].split(':')) > 2:
                            clean_ports.append(ports[i].split(':')[1])
                        else:
                            clean_ports.append(ports[i].split(':')[0])
                    print(clean_ports, type(clean_ports))
                    create_service(service, clean_ports)
                except Exception as err:  
                    logging.error(err)
                    pass        

def create_json():
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

    return json.dumps(data, indent=4)    


def change_ports(compose):
    with open(compose, 'r') as file:
        docker_config = yaml.load(file, Loader=yaml.FullLoader)
        # get services names
        services_names = docker_config['services'].keys()
        # convert to list
        services_names = list(services_names)
        for service in services_names:
            try:
                ports = docker_config['services'][service]['ports']
                clean_ports = []
                for i in range(len(ports)):
                    if len(ports[i].split(':')) > 2:
                        clean_ports.append(ports[i].split(':')[1])
                    else:
                        clean_ports.append(ports[i].split(':')[0])
                #print(clean_ports)
                for i in range(len(clean_ports)):
                    clean_ports[i] = str(int(clean_ports[i]) + 1)
                docker_config['services'][service]['ports'] = clean_ports
            except:
                pass
    with open(compose, 'w') as file:
        yaml.dump(docker_config, file, default_flow_style=False)

def edit_compose(folder):
    logging.info('[+] Start editing docker-compose.yml files')
    compose_files = glob.glob(os.path.join(folder, '**/docker-compose.yml'), recursive=True)
    compose_files = [x for x in compose_files if 'ctf_proxy' not in x]
    
    for compose_file in compose_files:
        compose_backup(compose_file)
        change_ports(compose_file)
        add_network(compose_file)
    
    logging.info('[+] Finished editing docker-compose.yml files')

if __name__ == "__main__":
    
    # start logging namee file logfile+timestamp
    logging.info("Start logging")
    
    # get all subfolders
    subfolders = [f.path for f in os.scandir('.') if f.is_dir() ]
    #print(subfolders)
    logging.info('[+] Get all subfolders')
    # remove all folders that start with .
    subfolders = [x for x in subfolders if not x.startswith('./.')]
    # remove all folders that end with ctf_proxy
    subfolders = [x for x in subfolders if not x.endswith('ctf_proxy')]

    data = get_docker_services(subfolders)
    
    json_data = create_json()
    logging.info('[+] Created data for config.json file')
    
    ## write data on config.json
    with open('./ctf_proxy/proxy/config/config.json', 'w') as outfile:
        outfile.write(json_data)
    logging.info('[+] Updated config.json file with new containers')


    ## edit docker-compose.yml files
    main_folder = os.getcwd()
    edit_compose(main_folder)