#!/usr/bin/python3
"""the city class file"""
from models.base_model import BaseModel


class City(BaseModel):
    """the class of the city
    Args:
        State_id (str): the id of the state (State.id)
        name (str): the name of the city
    """
    state_id = ""
    name = ""
