#!/usr/bin/python3
"""the main entry to the BaseModel for the ABnB console"""
import uuid
from datetime import datetime


class BaseModel:
    """the BaseModel class"""
    def __init__(self, *av, **kav):
        """init the BaseModel obj
        Args:
            av (list): the list of args , --not_used--
            kav (dict): the dictionnary of args
        """

        if kav:
            for key, value in kav.items():
                if (key == "__class__"):
                    continue
                elif (key == "created_at" or key == "updated_at"):
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            from models import storage
            storage.new(self)

    def __str__(self):
        """printable formatted stirng of the objj"""
        return (str("[{}] ({}) <{}>".format(self.__class__.__name__,
                                            self.id, self.__dict__)))

    def save(self):
        """update the updated_at attr"""
        self.updated_at = datetime.now()
        from models import storage
        storage.save()

    def to_dict(self):
        """return a dictionnary of the current class attributes
        as well as the base __dict__ containings"""
        dictionnary = self.__dict__.copy()
        dictionnary["__class__"] = self.__class__.__name__
        dictionnary["created_at"] = dictionnary["created_at"].isoformat()
        dictionnary["updated_at"] = dictionnary["updated_at"].isoformat()
        return (dictionnary)
