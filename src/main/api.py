import socket
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import uvicorn

import models
import database

# - App configs --------------------------
AppConf = models.AppSettings()

# - Initialiting Database & API -------------------
MyDB = database.MongoDatabase(mongohost="localhost", mongoport=27017)
MyDB.setup_connection(database_name="usersdb", collection_name="userscoll")

app = FastAPI()

# API AREA --------------------------------

# Root
@app.get('/')
async def root():
    hostname = socket.gethostname()

    resObj = {
        "hostname": hostname,
        "status_code": 200
    }
    return resObj

# Post User V1
@app.post('/api/v1/user')
async def post_user(user:models.User):

    print(user)
    data = jsonable_encoder(user)
    # user_dict = user.__dict__
    MyDB.insert_one(data)

    resObj = {
        "message": f"{user.first_name} added to Database.",
        "status_code": 200
    }

    return resObj

@app.get('/api/v1/users')
async def get_users():
    docuements = MyDB.find_all()

    resObj = {
        "documents": docuements,
        "status_code": 200
    }

    return resObj

@app.delete('/api/v1/user/{userid}')
async def delete_user(userid:str):
    MyDB.delete_user(userid)

    resObj = {
        "message": f"Userid {userid} deleted successfully.",
        "status_code": 200
    }

    return resObj

@app.put('/api/v1/user/{userid}')
async def update_user(user_id: str, user:models.User):

    MyDB.update_user(user_id, user)

    resObj = {
        "message": f"Benutzer {user_id} wurde aktualisiert!",
        "status_code": 200
    }

    return resObj

# The Runner -----------------------------------
if __name__ == "__main__":
    uvicorn.run(app="__main__:app", host="0.0.0.0", port=AppConf.api_port, reload=True)
