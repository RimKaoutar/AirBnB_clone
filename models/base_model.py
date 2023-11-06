#!/usr/bin/python3
"""the main entry to the BaseModel for the ABnB console"""
import uuid
import datetime
from models import storage


class BaseModel:
    """the BaseModel class"""
    def __init__(self, *args, **kwargs):
        """init the BaseModel obj"""
        if kwargs:
            pass
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """printable formatted stirng of the objj"""
        return (str("[{}] ({}) <{}>".format(self.__class__.__name__,
                                            self.id, self.__dict__)))

    def save(self):
        """update the updated_at attr"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """return a dictionnary of the current class attributes
        as well as the base __dict__ containings"""
        dictionnary = self.__dict__.copy()
        dictionnary["__class__"] = self.__class__.__name__
        dictionnary["crated_at"] = dictionnary["created_at"].isoformat()
        dictionnary["updated_at"] = dictionnary["updated_at"].isoformat()
        return (dictionnary)
