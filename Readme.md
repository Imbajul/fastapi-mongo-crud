# App API
Das ist eine API für ein beispiel

## Setup
```
pipenv shell
cd src
pip install -r requirements.txt
```

## Build container
```
docker build -t <DEINOIMAGENAME> .
```

## Die komplette Dockerfile zum verstädnis:
### Verwende das Python-Image als Basis
```
FROM python:3.11-slim
```
### Erstelle ein Verzeichnis namens "app" im Container
```
RUN mkdir /app
```
### Kopiere die Anforderungen (dependencies) von deinem lokalen "src" Ordner in den "/opt" Ordner im Container
```
COPY /src/requirements.txt /opt/requirements.txt
```
### Installiere die Anforderungen (dependencies) im Container mithilfe von pip
```
RUN pip install -r /opt/requirements.txt
```
### Kopiere den Hauptcode von deinem lokalen "src/main" Ordner in den "app" Ordner im Container
```
COPY /src/main /app
```
### Setze das Arbeitsverzeichnis (working directory) im Container auf den "app" Ordner
```
WORKDIR /app
```
### Starte den Befehl, der ausgeführt werden soll, wenn der Container gestartet wird
```
CMD ["python", "main.py"]
```
## Run container
```
docker run -dp 8000:5000 -e API_PORT=5000 <DEINOIMAGENAME>
```

```
-dp = detached, port forwarding
-e = ENV vars
```