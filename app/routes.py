from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from app.crud import add_guest_house, store_weather_forecast, delete_guest_house, update_guest_house, create_user, get_user_by_email
from app.weather import get_city_weather
from app.database import get_db
from sqlalchemy.orm import Session
from app.auth import authenticate_user, create_access_token, verify_token
from app.models import GuestHouse, WeatherData
from typing import Optional 
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer




router = APIRouter()



class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    

    new_user = create_user(db, email=user.email, password=user.password)
    return new_user



@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    #authenticate user
    db_user = authenticate_user(db, user.email, user.password)
    
    if db_user:
        #create JWT token
        access_token = create_access_token(data={"sub": db_user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

security = HTTPBearer()

class GuestHouseCreate(BaseModel):
    name: str
    location: str
    city: str
    amenities: str
    ratings: float
    places_nearby: str
    restaurants_cafes_nearby: str
    airports_nearby: str


@router.get("/guesthouses")
async def get_guesthouses(db: Session = Depends(get_db)):
    """
    Fetches a list of all guest houses.
    """
    try:
        guesthouses = db.query(GuestHouse).all()
        if not guesthouses:
            raise HTTPException(status_code=404, detail="No guest houses found")
        return guesthouses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/guesthouses")
async def create_guest_house(
    authorization: str = Header(None),
    data: dict = {},
    db: Optional[Session] = Depends(get_db)
):
    token = verify_token(authorization)
    add_guest_house(data, db)
    
    return {"message": "Guest house added successfully"}

@router.delete("/guesthouse/{guesthouse_id}")
async def delete_guesthouse(
    guesthouse_id: int,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    token = verify_token(authorization)

    return delete_guest_house(guesthouse_id, db)

@router.put("/guesthouse/{guesthouse_id}")
async def update_guesthouse(
    guesthouse_id: int,
    data: dict,
    authorization: str = Header(None),
    db: Session = Depends(get_db),
):

    token = verify_token(authorization)

    guesthouse = update_guest_house(guesthouse_id, data, db)
    return {"message": "Guesthouse updated successfully", "guesthouse": guesthouse}


@router.get("/weather/tunisia")
def save_weather_forecast(db: Session = Depends(get_db)):
    cities = ["Tunis", "Sfax", "Sousse", "Midoun", "Kairouan", "Bizerte", "Gabes", "Kasserine", "Gafsa", 
        "La Goulette", "Zarzis", "Monastir", "La Mohammedia", "La Marsa", "Masakin", "Saqanis", 
        "Houmt El Souk", "Tataouine", "El Hamma", "Douane", "Beja", "Hammamet", "Jendouba", "El Kef", 
        "Hammam-Lif", "Oued Lill", "Ferryville", "Mahdia", "Zouila", "Rades", "Kelibia", "Sidi Bouzid", 
        "Al Metlaoui", "Jammal", "Qasr Hallal", "Tozeur", "Dar Chabanne", "Hammam Sousse", "Al Qarmadah", 
        "Korba", "Mornag", "Mateur", "Redeyef", "Douz", "Ksour Essaf", "Siliana", "Manouba", "Nefta", 
        "Chebba", "Menzel Jemil", "Taklisah", "Majaz al Bab", "El Jem", "Akouda", "Kebili", "Tajerouine", 
        "Dawwar Tinjah", "Al Wardanin", "El Fahs", "Beni Khiar", "Zaghouan", "Manzil Bu Zalafah", "Al Aliyah", 
        "Thala", "Al Baqalitah", "Carthage", "Menzel Abderhaman", "Maktar", "Sahline", "As Sayyadah", 
        "Tabarka", "Tastur", "Bin Qirdan", "Tabursuq", "Bani Khallad", "Toujane", "Aghir", "Sulayman", "Tamezret"]  # Add your cities here
    for city in cities:
        weather_data = get_city_weather(city)
        if "error" not in weather_data:
            store_weather_forecast(city, weather_data, db)
    return {"message": "Weather forecasts for Tunisia stored successfully."}


WEATHER_DESCRIPTIONS = {
    "clearday": "clear weather day",
    "clearnight": "clear weather night",
    "pcloudyday": "a bit cloudy day",
    "pcloudynight": "a bit cloudy night",
    "mcloudyday": "cloudy day",
    "mcloudynight": "cloudy night",
    "cloudyday": "very cloudy day",
    "cloudynight": "very cloudy night",
    "humidday": "humid day",
    "humidnight": "humid night",
    "lightrainday": "light rain day",
    "lightrainnight": "light rain night",
    "oshowerday": "moderate rain day",
    "oshowernight": "moderate rain night",
    "ishowerday": "rainy day",
    "ishowernight": "rainy night",
    "rainday": "heavy rain day",
    "rainnight": "heavy rain night",
    "lightsnowday": "light snow day",
    "lightsnownight": "light snow night",
    "snowday": "heavy snow day",
    "snownight": "heavy snow night",
    "rainsnowday": "heavy freezing rain/possible ice pellets day",
    "rainsnownight": "heavy freezing rain/possible ice pellets night"
}

UNDESIRABLE_WEATHER = {
    "mcloudyday","mcloudynight","cloudyday","cloudynight","humidday","humidnight","lightrainday","lightrainnight","oshowerday",
    "oshowernight","ishowerday","ishowernight","rainday","rainnight","lightsnowday","lightsnownight","snowday","snownight",
    "rainsnowday","rainsnownight"
}

DESIRABLE_WEATHER = {
    "clearday", "clearnight", "pcloudyday", "pcloudynight"
}

WEATHER_MAPPING = {
    "clear weather day":"clearday",
    "clear weather night":"clearnight",
    "a bit cloudy day": "pcloudyday",
    "a bit cloudy night": "pcloudynight",
    "cloudy day": "mcloudyday",
    "cloudy night": "mcloudynight",
    "humid day": "humidday",
    "humid night": "humidnight",
    "light snow day": "lightsnowday",
    "light snow night": "lightsnownight",
    "very cloudy day": "cloudyday",
    "very cloudy night": "cloudynight",
    "light rain day": "lightrainday",
    "light rain night": "lightrainnight",
    "moderate rain day": "oshowerday",
    "moderate rain night": "oshowernight",
    "rainy day": "ishowerday",
    "rainy night": "ishowernight",
    "heavy rain day": "rainday",
    "heavy rain night": "rainnight",
    "heavy snow day": "snowday",
    "heavy snow night": "snownight",
    "heavy freezing rain/possible ice pellets day": "rainsnowday",
    "heavy freezing rain/possible ice pellets night": "rainsnownight"
}


@router.get("/guesthouses/{guesthouse_id}/weather/{selected_date}")
def get_weather_for_selected_date(guesthouse_id: int, selected_date: str, db: Session = Depends(get_db)):
    guesthouse = db.query(GuestHouse).filter(GuestHouse.id == guesthouse_id).first()
    if not guesthouse:
        raise HTTPException(status_code=404, detail="Guesthouse not found")
    
    weather_data = db.query(WeatherData).filter(WeatherData.city == guesthouse.city).all()
    if not weather_data:
        raise HTTPException(status_code=404, detail="Weather data not found for this city")
    
    try:
        selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Please use 'YYYY-MM-DD'.")
    
    weather_forecast = []
    guesthouse_weather = None
    base_time = datetime.now()
    for weather in weather_data:
        forecasted_datetime = base_time + timedelta(hours=weather.timepoint)
        if forecasted_datetime.date() == selected_date_obj.date():
            mapped_weather = WEATHER_MAPPING.get(weather.weather, weather.weather)
            weather_description = WEATHER_DESCRIPTIONS.get(mapped_weather, "Unknown weather")
            weather_forecast.append({
                "weather": weather_description,
                "city": weather.city,
                "forecasted_date": forecasted_datetime.strftime("%Y-%m-%d"),
                "forecasted_time": forecasted_datetime.strftime("%H:%M:%S"),
            })
            if weather.city == guesthouse.city:
                guesthouse_weather = mapped_weather

    if not weather_forecast:
        raise HTTPException(status_code=404, detail="No weather data available for the selected date.")
    
    undesirable_weather_occurrences = [
        mapped_weather for mapped_weather in WEATHER_MAPPING.values() if mapped_weather in UNDESIRABLE_WEATHER
    ]

    alternative_dates = []
    suggested_guesthouses = []

    if guesthouse_weather in UNDESIRABLE_WEATHER:
        for weather in weather_data:
            forecasted_datetime = base_time + timedelta(hours=weather.timepoint)
            mapped_weather = WEATHER_MAPPING.get(weather.weather, weather.weather)
            if forecasted_datetime.date() != selected_date_obj.date() and mapped_weather in DESIRABLE_WEATHER:
                alternative_dates.append({
                    "date": forecasted_datetime.strftime("%Y-%m-%d"),
                    "weather": WEATHER_DESCRIPTIONS.get(mapped_weather, "Unknown weather"),
                    "forecasted_time": forecasted_datetime.strftime("%H:%M:%S"),
                })
        
        if not alternative_dates:
            alternative_dates = "No better days found."
        
        for suggestion in db.query(GuestHouse).all():
            suggested_weather_data = db.query(WeatherData).filter(
                WeatherData.city == suggestion.city
            ).all()
            for suggested_weather in suggested_weather_data:
                forecasted_datetime = base_time + timedelta(hours=suggested_weather.timepoint)
                if forecasted_datetime.date() == selected_date_obj.date():
                    mapped_suggested_weather = WEATHER_MAPPING.get(suggested_weather.weather, suggested_weather.weather)
                    if mapped_suggested_weather in DESIRABLE_WEATHER:
                        suggested_guesthouses.append({
                            "id": suggestion.id,
                            "name": suggestion.name,
                            "city": suggestion.city,
                            "amenities": suggestion.amenities,
                            "places nearby": suggestion.places_nearby,
                            "restaurants and cafes nearby": suggestion.restaurants_cafes_nearby,
                            "airports nearby": suggestion.airports_nearby,
                            "weather": WEATHER_DESCRIPTIONS.get(mapped_suggested_weather, "Unknown weather"),
                            "forecasted_date": forecasted_datetime.strftime("%Y-%m-%d"),
                            "forecasted_time": forecasted_datetime.strftime("%H:%M:%S"),
                        })
                    break
        
        if not suggested_guesthouses:
            suggested_guesthouses = "No better options available."

    return {
        "guesthouse": {
            "id": guesthouse.id,
            "name": guesthouse.name,
            "location": guesthouse.location,
            "city": guesthouse.city,
            "amenities": guesthouse.amenities,
            "places nearby": guesthouse.places_nearby,
            "restaurants and cafes nearby": guesthouse.restaurants_cafes_nearby,
            "airports nearby": guesthouse.airports_nearby,
        },
        "weather_forecast": weather_forecast,
        "alternative_dates": alternative_dates,
        "suggested_guesthouses": suggested_guesthouses
    }
