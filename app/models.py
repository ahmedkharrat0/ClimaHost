# Database models
from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String) 




class GuestHouse(Base):
    __tablename__ = "guesthouses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    city = Column(String)
    amenities = Column(String)
    ratings = Column(Float)
    places_nearby = Column(String)
    restaurants_cafes_nearby = Column(String)
    airports_nearby = Column(String)
    

class WeatherData(Base):
    __tablename__ = "weather_data"
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    timepoint = Column(Integer)
    cloudcover = Column(Integer)
    lifted_index = Column(Integer)
    prec_type = Column(String)
    prec_amount = Column(Float)
    temp2m = Column(Float)
    rh2m = Column(String)
    wind_direction = Column(String)
    wind_speed = Column(Float)
    weather = Column(String)

    def __repr__(self):
        return f"<WeatherData(location={self.location}, temperature={self.temperature}, condition={self.weather_condition})>"