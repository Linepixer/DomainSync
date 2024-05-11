# Version ligera de python en docker
FROM python:3.12.3-alpine

# Seteo de directorio principal
WORKDIR /app

# Software principal y dependencias
COPY main.py requirements.txt ./

# Instalacion de dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Ejecucion de la aplicacion
CMD [ "python", "./main.py" ]
