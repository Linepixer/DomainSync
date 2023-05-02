#!/usr/bin/python
import json
import requests
from time import sleep
from godaddypy import Client, Account

version = "v1.1"
print("Starting DomainSync " + version)

public_key = ''
secret_key = ''

def get_public_ip():
	return requests.get("https://ipinfo.io/json", verify = True).json()['ip']

def get_old_public_ip():
    json_file = open("public_ip.json", "r")
    old_public_ip = json.load(json_file)["public_ip"]
    json_file.close()
    return old_public_ip

def dns_update(new_ip):
    client = Client(Account(api_key=public_key, api_secret=secret_key))
    if client.update_ip(new_ip, domains=['linepixer.com']) == True:
        json_file = open("public_ip.json", "w")
        json.dump({"public_ip":new_ip}, json_file)
        json_file.close()
        return
    else:
        raise

while True:
    try:
        public_ip = get_public_ip()
        old_public_ip = get_old_public_ip()
        if public_ip != old_public_ip:
            dns_update(public_ip)
            print("SUCESS: Domain updated")
        else:
            print("INFO: Without changes")
    except:
        print("ERROR: Failed to perform the operation")
    sleep(300)