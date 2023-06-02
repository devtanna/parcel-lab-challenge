import re
from typing import Optional

from django.core.cache import cache


class CacheMixin:
    @classmethod
    def sanitize_cache_key(cls, key:str) -> str:
        return re.sub(r'[^a-zA-Z0-9_]', '_', key)

    @classmethod
    def get_cached_data(cls, cache_key:str) -> dict:
        sanitized_key = cls.sanitize_cache_key(cache_key)
        return cache.get(sanitized_key)

    @classmethod
    def cache_data(cls, cache_key:str, data:dict, timeout: Optional[int]=None) -> None:
        sanitized_key = cls.sanitize_cache_key(cache_key)
        cache.set(sanitized_key, data, timeout)

class WeatherProviderBase:
    @classmethod
    def fetch_weather_data(cls, location:str, units:str) -> dict:
        raise NotImplementedError("Subclasses must implement get_weather_data method")

    @classmethod
    def get_weather(cls, location:str, units:str='metric') -> dict:
        return cls.fetch_weather_data(location, units=units)

    @classmethod
    def get_weather_emoji(cls, weather_code:str):
        weather_emojis = {
            '01': '☀️',  # Clear sky
            '02': '⛅️',  # Few clouds
            '03': '☁️',  # Scattered clouds
            '04': '☁️',  # Broken clouds
            '09': '🌧️',  # Shower rain
            '10': '🌦️',  # Rain
            '11': '⛈️',  # Thunderstorm
            '13': '🌨️',  # Snow
            '50': '🌫️',  # Mist
        }
        return weather_emojis.get(weather_code[:2], '🤷‍♂️')

class CachedWeatherProviderBase(CacheMixin, WeatherProviderBase):
    CACHE_TIMEOUT = 7200 # 2 hours

    @classmethod
    def fetch_weather_data(cls, location:str, units:str) -> dict:
        raise NotImplementedError("Subclasses must implement get_weather_data method")
    
    @classmethod
    def get_weather(cls, location:str, units:str ='metric') -> dict:
        cache_key = f'cached_weather_{location}_{units}'
        cached_data = cls.get_cached_data(cache_key)
        if cached_data:
            return cached_data
        weather_data = cls.fetch_weather_data(location, units=units)
        cls.cache_data(cache_key, weather_data, timeout=cls.CACHE_TIMEOUT)
        return weather_data
