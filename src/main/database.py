import pymongo
import models
from bson import ObjectId

class MongoDatabase():
    """
    Initializing MongoDB and conn.

    :Init Vars:
    mongohost = str
    mongoport = str

    :Methods:
    Setp connect: create db and coll
    """
    def __init__(self, mongohost:str, mongoport:int) -> None:
        self.monghost = mongohost
        self.mongoport =  mongoport
        self.myclient = None
        self.mydb = None
        self.mycoll = None

    def setup_connection(self, database_name:str, collection_name:str):
        uri = f"mongodb://{self.monghost}:{self.mongoport}/"
        self.myclient = pymongo.MongoClient(uri)
        self.mydb = self.myclient[database_name]
        self.mycoll = self.mydb[collection_name]

    def insert_one(self, item:models.User):
        self.mycoll.insert_one(item)

    def find_all(self) -> list:
        """
        Findet und gibt alle Dokumente in der MongoDB-Sammlung zurück.
        """
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

        query = {"_id": ObjectId(user_id)}
        new_values = {"$set": update_fields}
        self.mycoll.update_one(query, new_values)


