import socket                                   # Importieren Sie die socket-Bibliothek, um den Hostnamen zu erhalten.
import os                                       # Importieren Sie die os-Bibliothek, um das Datenverzeichnis einzurichten.
from fastapi import FastAPI, UploadFile, Depends, HTTPException, status         # Importieren Sie FastAPI und UploadFile für die API-Funktionalität.
from fastapi.encoders import jsonable_encoder   # Importieren Sie jsonable_encoder zum Codieren von Daten.
import uvicorn                                  # Importieren Sie uvicorn zum Ausführen des Servers.
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from typing import Annotated
from datetime import datetime, timedelta, timezone

import models                                   # Importieren Sie das Modul "models" für Datenmodelle.
import database                                 # Importieren Sie das Modul "database" für Datenbankoperationen.
from helpers import setup_data_dir              # Importieren Sie die setup_data_dir-Funktion aus dem Hilfsmodule.

# Importieren der fehlenden Funktionen und Klassen
from models import Token

# - App configs --------------------------
AppConf = models.AppSettings()                  # Initialisieren Sie die App-Konfigurationen aus den Modellen.
setup_data_dir()                                # Richten Sie das Datenverzeichnis ein.
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# - Initialiting Database & API -------------------
MyDB = database.MongoDatabase(mongohost=AppConf.mongohost, mongoport=AppConf.mongoport)                   # Initialisieren Sie die Datenbankverbindung.
MyDB.setup_connection(database_name="usersdb", collection_name="userscoll")             # Verbindung zur Datenbank und Sammlung herstellen.


app = FastAPI()                                 # Initialisieren Sie die FastAPI-Anwendung.

# -----------------------------------------Cryption 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def authenticate_user(username: str, password: str):
    user_list = MyDB.find_all()
    print(user_list)
    user = user_list[username]
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    
def get_password_hash(password):
        return pwd_context.hash(password)
    
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = models.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user_list = MyDB.find_all()
    print(user_list)
    user = user_list[token_data.username]
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[models.User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
# API AREA --------------------------------

# Root endpoint
@app.get('/')
async def root():
    hostname = socket.gethostname()             # Holen Sie sich den Hostnamen des Servers.

    resObj = {+
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

#-----------------------------------------------------------------------------------------------

@app.post('/api/v1/token') # <<<----
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get('/api/user/me/items/')
async def read_own_items(
    current_user: Annotated[models.User, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]

# The Runner with uvicorn (Server) # Führen Sie die FastAPI-Anwendung mit uvicorn aus.-----------------------------------
if __name__ == "__main__":
    uvicorn.run(app="__main__:app", host="0.0.0.0", port=AppConf.api_port, reload=False)  
