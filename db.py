from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def create_locations():
    locations = [
        {"name": "Cocktail Lounge", "latitude": 42.12345, "longitude": -76.54321},
        {"name": "Olin Library", "latitude": 42.12346, "longitude": -76.54322},
        {"name": "Slope", "latitude": 42.12350, "longitude": -76.54330},
        {"name": "Duffield Hall", "latitude": 42.44301, "longitude": -76.48410},
        {"name": "Tang Hall", "latitude": 42.44857, "longitude": -76.48399},
        {"name": "Statler Hall", "latitude": 42.44410, "longitude": -76.48240},
        {"name": "Kennedy Hall", "latitude": 42.44750, "longitude": -76.48480}
    ]
    for loc in locations:
        location = Location(name=loc['name'], latitude=loc['latitude'], longitude=loc['longitude'])
        db.session.add(location)
    db.session.commit()

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Location Model
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

# Post Model
class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    location_name = db.Column(db.String(100), nullable=False)  # Store location name directly
    content = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, location_name, content):
        self.user_id = user_id
        self.location_name = location_name 
        self.content = content
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "location_name": self.location_name,
            "content": self.content,
            "likes": self.likes,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }


from math import radians, cos, sin, sqrt, atan2

# Distance between two points on a sphere.
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Returns the nearest named location to a given longitude and latitude.
def get_nearest_location(latitude, longitude):
    locations = Location.query.all()
    nearest_location = None
    min_distance = float('inf')

    for location in locations:
        distance = haversine(latitude, longitude, location.latitude, location.longitude)
        if distance < min_distance:
            min_distance = distance
            nearest_location = location

    return nearest_location