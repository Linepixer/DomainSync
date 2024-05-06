#!venv/bin/python
import os
import requests
from time import sleep

# Version del software
version = "v2.1"
print("Starting DomainSync " + version)

# IP inicial
old_public_ip="0.0.0.0"

# Obtener IP publica
def get_public_ip():
	return requests.get("https://ipinfo.io/json", verify = True).json()['ip']

# Actualizacion de DNS
def dns_update(new_ip):
    params = {
            'key': os.getenv('API_KEY'),
            'command': 'set_dns2',
            'domain': 'linepixer.com',

            'main_record_type0': 'a',
            'main_record0':new_ip,

            'main_record_type1':'mx',
            'main_record1':'mx.zoho.com',
            'main_recordx1':'10',

            'main_record_type2':'mx',
            'main_record2':'mx2.zoho.com',
            'main_recordx2':'20',

            'main_record_type3':'mx',
            'main_record3':'mx3.zoho.com',
            'main_recordx3':'50',

            'main_record_type4':'txt',
            'main_record4':'v=spf1 include:zohomail.com ~all',

            'subdomain1':'www',
            'sub_record_type1':'a',
            'sub_record1':new_ip,

            'subdomain2':'cloud',
            'sub_record_type2':'a',
            'sub_record2':new_ip,

            'subdomain3':'play',
            'sub_record_type3':'a',
            'sub_record3':new_ip,

            'subdomain4':'zmail._domainkey',
            'sub_record_type4':'txt',
            'sub_record4':'v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCfg3Wi1CNsx0kNG2Pd45uCvXhjItjWVNbXSD3NyRv/t+D4PdVUe7JT3QFmkhrOdTvCM+i3OVGqHguzMRLD7CjDkAsmcEvMP0yrn3L8GdSDzz+TNb5CT8DLGEYJAL5pIJQEDYInNuHVsziqpNwL9zACZeJ0JbKn+OhP2G74IYEIdwIDAQAB',
            
            'subdomain5':'_dmarc',
            'sub_record_type5':'txt',
            'sub_record5':'v=DMARC1; p=quarantine; rua=mailto:diazmatias@linepixer.com; ruf=mailto:diazmatias@linepixer.com; sp=quarantine; adkim=r; aspf=r',

            'ttl':'300'
            }
    response = requests.get(f'https://api.dynadot.com/api3.json', params=params)
    if response.status_code == 200:
        response_code = response.json().get('SetDnsResponse', {}).get('ResponseCode')
        if response_code == 0:
            global old_public_ip
            old_public_ip = new_ip
            return
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
    except Exception as error:
        print("ERROR: Failed to perform the operation")
        print(error)
    sleep(180)