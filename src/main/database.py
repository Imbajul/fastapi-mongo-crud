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
        self.monghost = mongohost                               # Setzen Sie den Hostnamen der MongoDB.
        self.mongoport =  mongoport                             # Setzen Sie die Portnummer der MongoDB.
        self.myclient = None                                    # Initialisieren Sie den MongoDB-Client.
        self.mydb = None                                        # Initialisieren Sie die MongoDB-Datenbank.
        self.mycoll = None                                      # Initialisieren Sie die MongoDB-Sammlung.

    def setup_connection(self, database_name:str, collection_name:str):
        uri = f"mongodb://{self.monghost}:{self.mongoport}/"    # MongoDB-Verbindungs-URI erstellen.
        print(uri)
        self.myclient = pymongo.MongoClient(uri)                # MongoDB-Client erstellen.
        self.mydb = self.myclient[database_name]                # Datenbank auswählen.
        self.mycoll = self.mydb[collection_name]                # Sammlung auswählen.

    def insert_one(self, item:models.User):
        self.mycoll.insert_one(item)                            # Löschen Sie das Dokument mit der angegebenen ID.

        """
        Ein Dokument in die MongoDB-Sammlung einfügen.

        :param item: Das einzufügende Dokument.
        """

    def find_all(self) -> list:
        """
        Findet und gibt alle Dokumente in der MongoDB-Sammlung zurück.
        """
        cursor = self.mycoll.find({})
        docuements = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            docuements.append(doc)
        return docuements                                        # Rückgabe der Liste aller Dokumente.
    
    def delete_user(self, id:str):
        self.mycoll.delete_one({'_id': ObjectId(id)})            # Löschen Sie das Dokument mit der angegebenen ID.

    def update_user(self, user_id: str, user: models.User):
        update_fields = {}

# Überprüfen Sie jedes Feld des Benutzers und aktualisieren Sie es entsprechend.

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


