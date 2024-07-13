#!/usr/bin/env python3
from app import app
from models import db, Restaurant, Pizza, RestaurantPizza
import requests

BASE = 'http://127.0.0.1:5555'

response = requests.get(BASE + '/restaurants/1')
print(response.json())


