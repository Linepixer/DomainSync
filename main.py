#!/usr/bin/python
import json
import smtplib
import requests
from time import sleep

version = "v1.0"
print("Starting IP Change Detector " + version)

def get_public_ip():
	return requests.get("https://ipinfo.io/json", verify = True).json()['ip']

def get_old_public_ip():
    json_file = open("public_ip.json", "r")
    old_public_ip = json.load(json_file)["public_ip"]
    json_file.close()
    return old_public_ip

def write_new_public_ip(new_ip):
    json_file = open("public_ip.json", "w")
    json.dump({"public_ip":new_ip}, json_file)
    json_file.close()
    return

while True:
    try:
        public_ip = get_public_ip()
        old_public_ip = get_old_public_ip()
        if public_ip == old_public_ip:
            print("La IP no ha cambiado")
        else:
            mail_subject = "La IP del servidor cambio!"
            mail_text = "La IP publica del servidor cambio.\n\n" + \
                        "Direccion IP original: " + old_public_ip + "\n" + \
                        "Nueva direccion IP: " + public_ip
            mail_message = 'Subject: {}\n\n{}'.format(mail_subject, mail_text)
            gmail_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            gmail_server.login("linepixerserver@gmail.com", "PASSWORD_APP") # Colocar en el lugar de PASSWORD_APP la contraseña de la app
            gmail_server.sendmail("linepixerserver@gmail.com", "matiasezequieldiaz@yahoo.com.ar", mail_message)
            gmail_server.quit()
            write_new_public_ip(public_ip)
            print("La IP cambio")
    except:
        print("Fallo al realizar la operacion, revisar conexion a internet")
    sleep(300)