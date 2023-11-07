#!/usr/bin/python3
"""the review class file"""
from models.base_model import BaseModel


class Review(BaseModel):
    """the Review of a place
    Args:
        place_id (str): the place.id
        user_id (str): the user who published the review
        text (str): the rewiew
    """
    place_id = ""
    user_id = ""
    text = ""
