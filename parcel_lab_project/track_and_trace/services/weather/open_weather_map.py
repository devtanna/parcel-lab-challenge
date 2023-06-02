import logging

import requests
from django.conf import settings

from .base import CachedWeatherProviderBase

logger = logging.getLogger(__name__)

class OpenWeatherMapProvider(CachedWeatherProviderBase):
    @classmethod
    def fetch_weather_data(cls, location, units) -> dict:
            # first convert the location to lat/lon
            logger.info("Fetching lat/lon data from OpenCageData for location {location}")
            geocoding_url = f'{settings.OPENCAGE_API_URL}?q={location}&key={settings.OPENCAGE_API_KEY}'
            response = requests.get(geocoding_url)
            geocoding_data = response.json()
            if not response.ok:
                logger.error(f'Error fetching geocoding data from OpenCageData: {geocoding_data}')
                return {}
            
            lat = geocoding_data['results'][0]['geometry']['lat']
            lon = geocoding_data['results'][0]['geometry']['lng']
        
            logger.info(f"Fetching weather data from OpenWeatherMap for lat/lon {lat}/{lon}")
            weather_url = f'{settings.OPEN_WEATHER_API_URL}?lat={lat}&lon={lon}&appid={settings.OPEN_WEATHER_API_KEY}&units={units}'
            response = requests.get(weather_url)
            weather_data = response.json()
            if not response.ok:
                logger.error(f'Error fetching weather data from OpenWeatherMap: {weather_data}')
                return {}
            
            weather_code = weather_data['weather'][0]['icon']

            return {
                'weather_emoji': cls.get_weather_emoji(str(weather_code)) if weather_code else '🤷‍♂️',
                'temp': weather_data.get('main').get('temp'),
                'feels_like': weather_data.get('main').get('feels_like'),
                'temp_min': weather_data.get('main').get('temp_min'),
                'temp_max': weather_data.get('main').get('temp_max'),
            }
