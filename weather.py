import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = os.getenv("WEATHER_BASE_URL", "https://api.openweathermap.org/data/2.5/weather")


def get_weather(city: str) -> dict:
    """
    Отримує погоду для вказаного міста.
    
    Args:
        city: Назва міста
        
    Returns:
        dict: Словник з даними про погоду або None у разі помилки
        
    Raises:
        ValueError: Якщо API_KEY не встановлено
        requests.RequestException: У разі помилки HTTP-запиту
    """
    if not API_KEY:
        raise ValueError("WEATHER_API_KEY не встановлено в .env файлі")
    
    if not BASE_URL:
        raise ValueError("WEATHER_BASE_URL не встановлено в .env файлі")
    
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # для отримання температури в Цельсіях
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # викине виняток для статусів 4xx/5xx
        return f"The weather in {city} is {response.json()['main']['temp']}°C"
    except requests.RequestException as e:
        raise requests.RequestException(f"Помилка при отриманні погоди: {e}")

