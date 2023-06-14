import os
import yaml
import json
import requests

# check folder in current directory
def check_folder():
    # get current directory
    current_dir = os.getcwd()
    # get list of files and folders in current directory
    folders = []
    for entry in os.scandir(current_dir):
        if entry.is_dir() and not entry.name.startswith('.'):
            folders.append(entry.name)
    return folders


def check_docker_compose(folder):
    ports = []
    # chek docker-compose.yml in folder
    if 'docker-compose.yml' in os.listdir(folder) or 'docker-compose.yaml' in os.listdir(folder):
        if 'docker-compose.yml' in os.listdir(folder):
            fil = 'docker-compose.yml'
        else:
            fil = 'docker-compose.yaml'
        # parse docker-compose.yml
        with open(folder + "/" + fil) as file:
            compose_data = yaml.safe_load(file)
            for service_name, service_data in compose_data.get('services', {}).items():
                service_ports = service_data.get('ports', [])
                for port in service_ports:
                    if isinstance(port, str):
                # Se la porta è specificata come stringa nel formato 'host:container'
                # chek if formait is "ip:hostPort:containerPort"
                        if len(port.split(':')) == 3:
                            host_port = port.split(':')[1]
                            ports.append(int(host_port))
                        else:
                            host_port, _ = port.split(':')
                            ports.append(int(host_port))
                    elif isinstance(port, int):
                # Se la porta è specificata come intero
                        ports.append(port)
    else:
        # print scan dir result
        print(folder + ' not have docker-compose.yml')
        print(os.listdir(folder))
        return "Nop"
    
    ports_str = ','.join(map(str, ports))
    #print(ports_str)
    return ports_str

def create_json(port, list_dir):
    services = []
    for i in range(len(port)):
        service = {
            "name": list_dir[i],
            "target_ip": list_dir[i],
            "target_port": port[i],
            "listen_port": port[i]
        }
        
        # if localhost:port retrun an http response add http = True
        try:
            r = requests.get('http://localhost:' + str(port[i]))
            if r.status_code == 200:
                service['http'] = "true"
        except:
            pass
        services.append(service)
    
    data = {
        "services": services
    }
    
    return data                


def main():
    # get list of files and folders in current directory
    list_dir = check_folder()
    # check if folder exist
    if 'ctf_proxy' in list_dir:
        #remove folder from list
        list_dir.remove('ctf_proxy')
    port = []
    print(list_dir)
    for folder in list_dir:
        port.append(check_docker_compose(folder))
    print(port)
        
    data = create_json(port, list_dir)
    json_data = json.dumps(data, indent=4)
    
    with open('config.json', 'w') as outfile:
        outfile.write(json_data)
        
if __name__ == '__main__':
    main()
    
