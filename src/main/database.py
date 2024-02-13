import pymongo
import models
from models import User
from bson import ObjectId
from helpers import hash_password


class MongoDatabase():
    def __init__(self, mongohost:str, mongoport:int) -> None:
        self.monghost = mongohost
        self.mongoport =  mongoport
        self.myclient = None
        self.mydb = None
        self.mycoll = None

    def setup_connection(self, database_name:str, collection_name:str):
        uri = f"mongodb://{self.monghost}:{self.mongoport}/"
        print(uri)
        self.myclient = pymongo.MongoClient(uri)
        self.mydb = self.myclient[database_name]
        self.mycoll = self.mydb[collection_name]

    def insert_one(self, item:models.User):
        self.mycoll.insert_one(item)

    def find_all(self) -> list:
        cursor = self.mycoll.find({})
        docuements = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            docuements.append(doc)
        return docuements
    
    def delete_user(self, id:str):
        self.mycoll.delete_one({'_id': ObjectId(id)})

    def update_user(self, user_id: str, user: models.User):
        update_fields = {}
        
        if user.first_name is not None:
            update_fields["first_name"] = user.first_name
        if user.last_name is not None:
            update_fields["last_name"] = user.last_name
        if user.age is not None:
            update_fields["age"] = user.age
        if user.gender is not None:
            update_fields["gender"] = user.gender
        if user.admin is not None:
            update_fields["admin"] = user.admin
        if user.admin is not None: 
            update_fields["email"] = user.email
        if user.username is not None:
            update_fields ["username"] = user.username
        if user.password is not None: 
            hashed_password = hash_password(user.password)        
            update_fields["password"] = hashed_password

        query = {"_id": ObjectId(user_id)}
        new_values = {"$set": update_fields}
        self.mycoll.update_one(query, new_values)
