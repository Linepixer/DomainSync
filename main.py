#!venv/bin/python
import os
import json
import requests
from time import sleep
from godaddypy import Client, Account

# Version del software
version = "v1.2"
print("Starting DomainSync " + version)

# Autentificacion
public_key = os.getenv('PUBLIC_KEY')
secret_key = os.getenv('SECRET_KEY')

# IP inicial
old_public_ip="0.0.0.0"

# Obtener IP publica
def get_public_ip():
	return requests.get("https://ipinfo.io/json", verify = True).json()['ip']

# Actualizacion de DNS
def dns_update(new_ip):
    global old_public_ip
    client = Client(Account(api_key=public_key, api_secret=secret_key))
    if client.update_ip(new_ip, domains=['linepixer.com']) == True:
        old_public_ip = new_ip
    else:
        raise

# Bucle principal
while True:
    try:
        public_ip = get_public_ip()
        if public_ip != old_public_ip:
            dns_update(public_ip)
            print(f"SUCESS: Domain updated to {public_ip}")
        else:
            print("INFO: Without changes")
    except KeyboardInterrupt:
        print("INFO: Stopping DomainSync")
        break
    except Exception as e:
        print("ERROR: Failed to perform the operation")
        print(e)
    sleep(180)
