#!/usr/bin/python3
"""the user class file"""
from models.base_model import BaseModel


class User(BaseModel):
    """the class of the user
    Args:
        email (str): the email of the user
        password (str): the password of the user
        first_name (str): the fisrt name
        last_name (str): the last name
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
