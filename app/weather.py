import requests

BASE_URL = "http://www.7timer.info/bin/api.pl"

def get_city_weather(city):
    city_coordinates = {
    "Tunis": (36.8065, 10.1815),
    "Sfax": (34.7407, 10.7615),
    "Sousse": (35.8256, 10.6369),
    "Midoun": (33.5028, 10.9022),
    "Kairouan": (35.6611, 10.1000),
    "Bizerte": (37.2740, 9.8730),
    "Gabes": (33.8833, 10.0986),
    "Kasserine": (35.1667, 8.8333),
    "Gafsa": (34.4230, 8.7762),
    "La Goulette": (36.8381, 10.3275),
    "Zarzis": (33.5280, 11.0106),
    "Monastir": (35.7771, 10.8250),
    "La Mohammedia": (35.8833, 10.2667),
    "La Marsa": (36.8647, 10.3227),
    "Masakin": (35.6500, 10.3500),
    "Saqanis": (35.3422, 10.2067),
    "Houmt El Souk": (33.8725, 10.8697),
    "Tataouine": (32.9300, 10.5067),
    "El Hamma": (33.4175, 10.4600),
    "Douane": (34.5833, 9.3667),
    "Beja": (36.7250, 9.1822),
    "Hammamet": (36.4000, 10.6094),
    "Jendouba": (36.5000, 8.7790),
    "El Kef": (36.1667, 8.7033),
    "Hammam-Lif": (36.7283, 10.2486),
    "Oued Lill": (36.7300, 9.4900),
    "Ferryville": (37.0333, 9.6833),
    "Mahdia": (35.5078, 11.0628),
    "Zouila": (34.7139, 10.3739),
    "Rades": (36.7492, 10.2692),
    "Kelibia": (36.8306, 11.1722),
    "Sidi Bouzid": (34.7333, 9.4833),
    "Al Metlaoui": (34.2425, 8.9050),
    "Jammal": (35.6100, 10.5000),
    "Qasr Hallal": (35.4792, 10.2978),
    "Tozeur": (33.9185, 8.1229),
    "Dar Chabanne": (35.6194, 10.0511),
    "Hammam Sousse": (35.8328, 10.6328),
    "Al Qarmadah": (35.5625, 10.3519),
    "Korba": (36.5117, 10.7033),
    "Mornag": (36.7000, 10.3736),
    "Mateur": (37.0911, 9.1292),
    "Redeyef": (33.7044, 8.6533),
    "Douz": (33.5014, 9.0056),
    "Ksour Essaf": (35.5992, 10.0694),
    "Siliana": (36.0833, 9.3700),
    "Manouba": (36.7556, 9.9875),
    "Nefta": (33.8744, 8.6242),
    "Chebba": (35.3500, 11.0247),
    "Menzel Jemil": (37.0236, 9.3031),
    "Taklisah": (35.9925, 10.0742),
    "Majaz al Bab": (36.4975, 9.6481),
    "El Jem": (35.2814, 10.7117),
    "Akouda": (35.7100, 10.5611),
    "Kebili": (33.7014, 8.9731),
    "Tajerouine": (34.6989, 9.3506),
    "Dawwar Tinjah": (35.4792, 10.2208),
    "Al Wardanin": (35.3994, 10.7261),
    "El Fahs": (36.5000, 9.7500),
    "Beni Khiar": (36.8000, 10.6000),
    "Zaghouan": (36.4069, 9.5072),
    "Manzil Bu Zalafah": (35.8933, 10.2667),
    "Al Aliyah": (35.8083, 10.0208),
    "Thala": (35.1775, 8.8167),
    "Al Baqalitah": (35.6833, 10.3000),
    "Carthage": (36.8500, 10.3233),
    "Menzel Abderhaman": (37.0172, 9.8578),
    "Maktar": (36.9500, 9.2833),
    "Sahline": (35.7439, 10.6417),
    "As Sayyadah": (35.9728, 9.6342),
    "Tabarka": (36.8808, 8.7506),
    "Tastur": (35.7050, 10.1456),
    "Bin Qirdan": (33.8833, 10.0833),
    "Tabursuq": (35.4800, 9.4833),
    "Bani Khallad": (35.3667, 10.0000),
    "Toujane": (33.4660, 10.1325),
    "Aghir": (33.7659, 11.0189),
    "Sulayman": (36.6966, 10.4931),
    "Tamezret": (33.5349, 9.8641),
    }

    if city not in city_coordinates:
        return {"error": "City not found in the predefined list."}
    
    lat, lon = city_coordinates[city]
    
    params = {
        'lon': lon,
        'lat': lat,
        'product': 'civil',
        'output': 'json'
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        weather_data = response.json()
        
        if "error" in weather_data:
            return weather_data 
        
        forecast_data = []
        for entry in weather_data.get('dataseries', []):
            forecast_data.append({
                'timepoint': entry.get('timepoint'),
                'cloudcover': entry.get('cloudcover'),
                'lifted_index': entry.get('lifted_index'),
                'prec_type': entry.get('prec_type'),
                'prec_amount': entry.get('prec_amount'),
                'temp2m': entry.get('temp2m'),
                'rh2m': entry.get('rh2m'),
                'wind10m': {
                    'direction': entry.get('wind10m', {}).get('direction'),
                    'speed': entry.get('wind10m', {}).get('speed')
                },
                'weather': entry.get('weather')
            })
        
        return forecast_data

    except requests.exceptions.RequestException as e:
        return {"error": f"API request error: {str(e)}"}

if __name__ == "__main__":
    city = "Tunis"
    print(get_city_weather(city))
