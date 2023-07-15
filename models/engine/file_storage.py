#!/usr/bin/python3
"""This module is responsible for serializing and deserializing
objects to/from a file"""
import os
import json
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
        return FileStorage.__objects

    def new(self, obj):
        """Adds a new object to the storage"""
        # making the key in this format <class name>.id
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            # k = classname.id and v = obj/an instance
            _dict = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
            json.dump(_dict, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        # if exists(self.__file_path)
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
            objdict = json.load(f)
            objdict = {k: FileStorage.__class_map[v["__class__"]](**v)
                       for k, v in objdict.items()}
            FileStorage.__objects = objdict

    @property
    def class_map(self):
        """Getter function for __class_map"""
        return self.__class_map
