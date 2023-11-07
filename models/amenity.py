#!/usr/bin/python3
""" the amenity class file"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """the Amenity of the Place
    Args:
        name (str): the name of the amenity
    """
    name = ""
