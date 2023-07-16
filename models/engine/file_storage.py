import os
import json
import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """File storage class, handles serialization and deserialization
    of json file"""
    __file_path = "file.json"
    __objects = {}
    __class_map = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def all(self):
        """Returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """Adds a new object to the storage"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        _dict = {k: v.to_dict() for k, v in self.__objects.items()}
        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(_dict, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        if os.path.isfile(self.__file_path):
            with open(self.__file_path, "r", encoding="utf-8") as f:
                objdict = json.load(f)
                for k, v in objdict.items():
                    class_name = v["__class__"]
                    self.__objects[k] = self.__class_map[class_name](**v)

    @property
    def class_map(self):
        """Getter function for __class_map"""
        return self.__class_map

    def attributes(self):
        """Returns the valid attributes and their types for each class"""
        attrs = {
            "BaseModel": {
                "id": str,
                "created_at": datetime.datetime,
                "updated_at": datetime.datetime
            },
            "User": {
                "email": str,
                "password": str,
                "first_name": str,
                "last_name": str
            },
            "State": {
                "name": str
            },
            "City": {
                "state_id": str,
                "name": str
            },
            "Amenity": {
                "name": str
            },
            "Place": {
                "city_id": str,
                "user_id": str,
                "name": str,
                "description": str,
                "number_rooms": int,
                "number_bathrooms": int,
                "max_guest": int,
                "price_by_night": int,
                "latitude": float,
                "longitude": float,
                "amenity_ids": list
            },
            "Review": {
                "place_id": str,
                "user_id": str,
                "text": str
            }
        }
        return attrs
