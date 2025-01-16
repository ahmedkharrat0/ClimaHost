from fastapi import FastAPI
#from app.routes import router as guesthouse_router
from app.database import engine, Base, SessionLocal
from app.weather import get_city_weather
from app.crud import store_weather_forecast, store_guest_houses_from_csv
from app.routes import router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()

app.include_router(router)
app.mount("/static", StaticFiles(directory="/guesthousesapi/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specific domains like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("templates/index.html", "r") as file:
        return file.read()

file_path = '/app/guesthouses.csv'

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    file_path = '/app/guesthouses.csv'
    with SessionLocal() as db:
        store_guest_houses_from_csv(file_path, db)
        
    cities = ["Tunis", "Sfax", "Sousse", "Midoun", "Kairouan", "Bizerte", "Gabes", "Kasserine", "Gafsa", 
        "La Goulette", "Zarzis", "Monastir", "La Mohammedia", "La Marsa", "Masakin", "Saqanis", 
        "Houmt El Souk", "Tataouine", "El Hamma", "Douane", "Beja", "Hammamet", "Jendouba", "El Kef", 
        "Hammam-Lif", "Oued Lill", "Ferryville", "Mahdia", "Zouila", "Rades", "Kelibia", "Sidi Bouzid", 
        "Al Metlaoui", "Jammal", "Qasr Hallal", "Tozeur", "Dar Chabanne", "Hammam Sousse", "Al Qarmadah", 
        "Korba", "Mornag", "Mateur", "Redeyef", "Douz", "Ksour Essaf", "Siliana", "Manouba", "Nefta", 
        "Chebba", "Menzel Jemil", "Taklisah", "Majaz al Bab", "El Jem", "Akouda", "Kebili", "Tajerouine", 
        "Dawwar Tinjah", "Al Wardanin", "El Fahs", "Beni Khiar", "Zaghouan", "Manzil Bu Zalafah", "Al Aliyah", 
        "Thala", "Al Baqalitah", "Carthage", "Menzel Abderhaman", "Maktar", "Sahline", "As Sayyadah", 
        "Tabarka", "Tastur", "Bin Qirdan", "Tabursuq", "Bani Khallad", "Toujane", "Aghir", "Sulayman", "Tamezret"]
    weather_data = {}
    for city in cities:
        city_weather = get_city_weather(city)
        if "error" not in city_weather:
            weather_data[city] = city_weather

    with SessionLocal() as db:
        for city, forecast in weather_data.items():
            store_weather_forecast(city, forecast, db)
    print("Weather data for Tunisia stored successfully.")


Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")

weather_data = get_city_weather("Tunis")
print("Weather data for Tunisia fetched successfully.")