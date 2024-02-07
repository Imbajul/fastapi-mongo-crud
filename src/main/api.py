import socket                                   # Importieren Sie die socket-Bibliothek, um den Hostnamen zu erhalten.
import os                                       # Importieren Sie die os-Bibliothek, um das Datenverzeichnis einzurichten.
from fastapi import FastAPI, UploadFile         # Importieren Sie FastAPI und UploadFile für die API-Funktionalität.
from fastapi.encoders import jsonable_encoder   # Importieren Sie jsonable_encoder zum Codieren von Daten.
import uvicorn                                  # Importieren Sie uvicorn zum Ausführen des Servers.

import models                                   # Importieren Sie das Modul "models" für Datenmodelle.
import database                                 # Importieren Sie das Modul "database" für Datenbankoperationen.
from helpers import setup_data_dir              # Importieren Sie die setup_data_dir-Funktion aus dem Hilfsmodule.

# - App configs --------------------------
AppConf = models.AppSettings()                  # Initialisieren Sie die App-Konfigurationen aus den Modellen.
setup_data_dir()                                # Richten Sie das Datenverzeichnis ein.

# - Initialiting Database & API -------------------
MyDB = database.MongoDatabase(mongohost=AppConf.mongohost, mongoport=AppConf.mongoport)                   # Initialisieren Sie die Datenbankverbindung.
MyDB.setup_connection(database_name="usersdb", collection_name="userscoll")             # Verbindung zur Datenbank und Sammlung herstellen.

app = FastAPI()                                 # Initialisieren Sie die FastAPI-Anwendung.

# API AREA --------------------------------

# Root endpoint
@app.get('/')
async def root():
    hostname = socket.gethostname()             # Holen Sie sich den Hostnamen des Servers.

    resObj = {
        "hostname": hostname,                   # Fügen Sie den Hostnamen zum Antwortobjekt hinzu.
        "status_code": 200                      # Geben Sie einen Statuscode zurück.
    }
    return resObj                               # Rückgabe des Antwortobjekts.

# Post User V1 endpoint
@app.post('/api/v1/user')
async def post_user(user:models.User):
    """
    Erstellt einen neuen Benutzer in der Datenbank.

    :param request_data: Anforderungskörper, der das Pydantic-Modell "User" verwendet.
    :return: Erfolgsmeldung
    """

    print(user)                                 # Geben Sie die Benutzerdaten aus.
    data = jsonable_encoder(user)               # Codieren Sie die Benutzerdaten.
    MyDB.insert_one(data)                       # Fügen Sie den Benutzer in die Datenbank ein.

    resObj = {
        "message": f"{user.first_name} wurde zur Datenbank hinzugefügt.",  # Erstellen Sie eine Erfolgsmeldung mit dem Benutzernamen.
        "status_code": 200                                                 # Geben Sie einen Statuscode zurück.
    }

    return resObj                               # Rückgabe des Antwortobjekts.

# Get Users endpoint
@app.get('/api/v1/users')
async def get_users():
    documents = MyDB.find_all()                 # Holen Sie sich alle Benutzerdokumente aus der Datenbank.

    resObj = {
        "documents": documents,                 # Fügen Sie die Benutzerdokumente zum Antwortobjekt hinzu.
        "status_code": 200                      # Geben Sie einen Statuscode zurück.
    }

    return resObj                               # Rückgabe des Antwortobjekts.

# Delete User endpoint
@app.delete('/api/v1/user/{userid}')
async def delete_user(userid:str):
    MyDB.delete_user(userid)                    # Löschen Sie den Benutzer mit der angegebenen Benutzer-ID aus der Datenbank.

    resObj = {
        "message": f"Benutzer mit ID {userid} erfolgreich gelöscht.",  # Erstellen Sie eine Erfolgsmeldung mit der Benutzer-ID.
        "status_code": 200                      # Geben Sie einen Statuscode zurück.
    }

    return resObj                               # Rückgabe des Antwortobjekts.

# Update User endpoint
@app.put('/api/v1/user/{userid}')
async def update_user(user_id: str, user:models.User):
    MyDB.update_user(user_id, user)             # Aktualisieren Sie den Benutzer mit der angegebenen Benutzer-ID in der Datenbank.

    resObj = {
        "message": f"Benutzer mit ID {user_id} wurde erfolgreich aktualisiert.",  # Erstellen Sie eine Erfolgsmeldung mit der Benutzer-ID.
        "status_code": 200                      # Geben Sie einen Statuscode zurück.
    }

    return resObj                               # Rückgabe des Antwortobjekts.

# Upload File endpoint
@app.post('/api/v1/upload')
async def upload_file(file: UploadFile):
    with open (f"{AppConf.data_dir}/{file.filename}", 'wb') as f:  # Öffnen Sie eine Datei im Datenverzeichnis im Schreibmodus.
        content = await file.read()             # Lesen Sie den Inhalt der hochgeladenen Datei.
        f.write(content)                        # Schreiben Sie den Inhalt in die Datei.

    resObj = {
        "message": f"{file.filename} erfolgreich hochgeladen.",  # Erstellen Sie eine Erfolgsmeldung mit dem Dateinamen.
        "status_code": 200                      # Geben Sie einen Statuscode zurück.
    }

    return resObj                               # Rückgabe des Antwortobjekts.

# The Runner -----------------------------------
if __name__ == "__main__":
    uvicorn.run(app="__main__:app", host="0.0.0.0", port=AppConf.api_port, reload=False)  # Führen Sie die FastAPI-Anwendung mit uvicorn aus.

