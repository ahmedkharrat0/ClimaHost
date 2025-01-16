
from app.models import GuestHouse, WeatherData, User
from sqlalchemy.orm import Session
from app.weather import get_city_weather
import pandas as pd
from passlib.context import CryptContext
from fastapi import HTTPException



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def create_user(db: Session, email: str, password: str):
    hashed_password = pwd_context.hash(password)
    new_user = User(email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

file_path = '/app/guesthouses.csv'


def store_guest_houses_from_csv(file_path: str, db: Session):
    guesthouses = pd.read_csv(file_path)
    
    for index, guesthouse in guesthouses.iterrows():
        existing_guesthouse = db.query(GuestHouse).filter(GuestHouse.name == guesthouse['name']).first()
        
        if existing_guesthouse is None:
            new_guesthouse = GuestHouse(
                id=guesthouse['id'],
                name=guesthouse['name'],
                location=guesthouse['location'],
                city=guesthouse['city'],
                amenities=guesthouse['amenities'],
                ratings=guesthouse['ratings'],
                places_nearby=guesthouse['places_nearby'],
                restaurants_cafes_nearby=guesthouse['restaurants_cafes_nearby'],
                airports_nearby=guesthouse['airports_nearby']
            )
            db.add(new_guesthouse)
    
    db.commit()


def get_guest_houses(db: Session):
    return db.query(GuestHouse).all() 

def add_guest_house(data: dict, db: Session):
    new_guest_house = GuestHouse(
        name=data['name'],
        location=data['location'],
        city=data['city'],
        amenities=data['amenities'],
        ratings=data['ratings'],
        places_nearby=data['places_nearby'],
        restaurants_cafes_nearby=data['restaurants_cafes_nearby'],
        airports_nearby=data['airports_nearby'],
    )
    db.add(new_guest_house)
    db.commit()
    db.refresh(new_guest_house)
    return new_guest_house

def delete_guest_house(guesthouse_id: int, db: Session):
    guesthouse = db.query(GuestHouse).filter(GuestHouse.id == guesthouse_id).first()
    
    if guesthouse:
        db.delete(guesthouse)
        db.commit()
        print(f"Guesthouse with ID {guesthouse_id} deleted successfully.")
        return {"message": f"Guesthouse with ID {guesthouse_id} deleted successfully."}
    else:
        print(f"Guesthouse with ID {guesthouse_id} not found.")
        raise HTTPException(status_code=404, detail="Guest house not found")

def update_guest_house(guesthouse_id: int, data: dict, db: Session):
    """
    Updates a guesthouse's attributes by its ID.
    """
    guesthouse = db.query(GuestHouse).filter(GuestHouse.id == guesthouse_id).first()

    if guesthouse:
        for key, value in data.items():
            if hasattr(guesthouse, key):
                setattr(guesthouse, key, value)
        
        db.commit()
        db.refresh(guesthouse)
        print(f"Guesthouse with ID {guesthouse_id} updated successfully.")
        return guesthouse
    else:
        print(f"Guesthouse with ID {guesthouse_id} not found.")
        raise HTTPException(status_code=404, detail="Guesthouse not found")


def create_weather_data(db: Session, weather_data: WeatherData):
    db.add(weather_data)
    db.commit()
    db.refresh(weather_data)
    return weather_data


def store_weather_forecast(city: str, forecast: dict, db: Session):
    try:
        for entry in forecast:
            weather_entry = WeatherData(
                city=city,
                timepoint=entry.get('timepoint'),
                cloudcover=entry.get('cloudcover'),
                lifted_index=entry.get('lifted_index'),
                prec_type=entry.get('prec_type'),
                prec_amount=entry.get('prec_amount'),
                temp2m=entry.get('temp2m'),
                rh2m=entry.get('rh2m'),
                wind_direction=entry['wind10m'].get('direction'),
                wind_speed=entry['wind10m'].get('speed'),
                weather=entry.get('weather')
            )
            db.add(weather_entry)
        db.commit()
        db.refresh(weather_entry)
        print(f"Weather data for {city} stored successfully.")
    except Exception as e:
        print(f"Error storing weather data for {city}: {str(e)}")


def fetch_and_store_weather_for_all_cities(db: Session):    
    tunisian_cities = [
        "Tunis", "Sfax", "Sousse", "Midoun", "Kairouan", "Bizerte", "Gabes", "Kasserine", "Gafsa", 
        "La Goulette", "Zarzis", "Monastir", "La Mohammedia", "La Marsa", "Masakin", "Saqanis", 
        "Houmt El Souk", "Tataouine", "El Hamma", "Douane", "Beja", "Hammamet", "Jendouba", "El Kef", 
        "Hammam-Lif", "Oued Lill", "Ferryville", "Mahdia", "Zouila", "Rades", "Kelibia", "Sidi Bouzid", 
        "Al Metlaoui", "Jammal", "Qasr Hallal", "Tozeur", "Dar Chabanne", "Hammam Sousse", "Al Qarmadah", 
        "Korba", "Mornag", "Mateur", "Redeyef", "Douz", "Ksour Essaf", "Siliana", "Manouba", "Nefta", 
        "Chebba", "Menzel Jemil", "Taklisah", "Majaz al Bab", "El Jem", "Akouda", "Kebili", "Tajerouine", 
        "Dawwar Tinjah", "Al Wardanin", "El Fahs", "Beni Khiar", "Zaghouan", "Manzil Bu Zalafah", "Al Aliyah", 
        "Thala", "Al Baqalitah", "Carthage", "Menzel Abderhaman", "Maktar", "Sahline", "As Sayyadah", 
        "Tabarka", "Tastur", "Bin Qirdan", "Tabursuq", "Bani Khallad", "Toujane", "Aghir", "Sulayman", "Tamezret"
    ]

    for city in tunisian_cities:
        print(f"Fetching weather data for {city}...")
        city_weather = get_city_weather(city)
        
        if "error" in city_weather:
            print(f"Error fetching data for {city}: {city_weather['error']}")
        else:
            store_weather_forecast(city, city_weather['forecast'], db)
            print(f"Weather data for {city} stored successfully.")


def test_db_connection(db: Session):
    result = db.query(WeatherData).all()
    print(f"WeatherData Table Records: {result}")
