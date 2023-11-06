#!/usr/bin/python3
"""Defines a class FileStorage."""
import json
import os


class FileStorage:
    __file_path = "file.json"
    __objects = dict()

    def all(self):
        """Returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        obj_name = obj.__class__.__name__
        key = f"{obj_name}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """ Serializes __objects to the JSON file """
        objs = {
            key: value.to_dict() for key, value in FileStorage.__objects.items()
        }
        with open(FileStorage.__file_path, mode = "w", encoding = "utf-8") as f:
            json.dump(objs, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        if os.path.exists(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r", encoding = "utf-8") as f:
                obj = json.load(f)
                self.new(obj)
