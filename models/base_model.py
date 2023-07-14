#!/usr/bin/python3
"""BaseModel class: defines all common attributes/methods for other classes"""

import uuid
from datetime import datetime
# used instead of "from models import storage" to supress circular imports
import models


class BaseModel:
    """Base class"""

    def __init__(self, *args, **kwargs):
        """Initializes a new instance of the BaseModel class"""
        if kwargs is not None and kwargs != {}:
            # Removes __class__ attr so as not to be added as an instance attr
            # when recreating the instance from the dictionary representation
            kwargs.pop('__class__', None)
            for key in kwargs:
                # strptime, str parse time: converts a str to datetime object
                if key == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[key] = kwargs[key]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def save(self):
        """Updates the `updated_at` attribute with the current datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary representation of the instance"""
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict

    def __str__(self):
        """Returns a string representation of the instance"""
        return "[{}] ({}) {}".\
            format(self.__class__.__name__, self.id, self.__dict__)
