#!/usr/bin/python3
"""the place class file"""
from models.base_model import BaseModel


class Place(BaseModel):
    """the class of the Place
    Args:
        city_id (str): the id of the place's city (City.id)
        user_id (str): the id of the user who booked the place
        (User.id)
        name (str): the name
        description (str): the desc of the place
        number_rooms (int): the number of the rooms
        number_bathrooms (int) : the number of the bathrooms
        max_guest (int): the max nbr of guests of the place
        price_by_night (int): the price of the place
        latitude (float): the latitude of the place
        longitude (float): the longitude of the place
        amenity_ids (list): a list of amenities (Amenity.id)
    """
    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
