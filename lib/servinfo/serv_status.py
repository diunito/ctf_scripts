#!/bin/false
import pwn
import requests

def check_web(ip, port, path=""):
    response = requests.get(f"http://{ip}:{port}/{path}")
    if response.status_code == 200: # service should be working fine
        return True
    else:
        return False

def check_tcp(ip, port):
    try:
        r = pwn.remote(ip, port)
        if r.recv(1, timeout=3) == b'': # timed out
            return False
        else: # service should be working fine
            return True
    except EOFError: # if nothing was sent
        return False
    except pwn.pwnlib.exception.PwnlibException: # if couldn't connect
        return False
