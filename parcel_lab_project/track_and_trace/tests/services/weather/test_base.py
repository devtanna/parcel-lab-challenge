import pytest
from django.core.cache import cache

from track_and_trace.services.weather.base import (CachedWeatherProviderBase,
                                                   CacheMixin,
                                                   WeatherProviderBase)


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()

@pytest.fixture
def weather_provider():
    return WeatherProviderBase()

@pytest.fixture
def cached_weather_provider():
    return CachedWeatherProviderBase()

def test_sanitize_cache_key():
    cache_key = "some_key!@#"
    expected_sanitize_key = "some_key___"
    assert CacheMixin.sanitize_cache_key(cache_key) == expected_sanitize_key

def test_get_cached_data(cached_weather_provider):
    cache_key = "cached_weather_Berlin_metric"
    expected_data = {"temperature": 20, "humidity": 80}
    cache.set(cache_key, expected_data)
    assert cached_weather_provider.get_cached_data(cache_key) == expected_data

def test_cache_data(cached_weather_provider):
    cache_key = "cached_weather_Berlin_metric"
    data = {"temperature": 20, "humidity": 80}
    cached_weather_provider.cache_data(cache_key, data)
    assert cache.get(cache_key) == data

def test_fetch_weather_data(weather_provider):
    with pytest.raises(NotImplementedError):
        weather_provider.fetch_weather_data("Berlin", "metric")

def test_get_weather(weather_provider):
    location = "Berlin"
    units = "metric"
    with pytest.raises(NotImplementedError):
        weather_provider.get_weather(location, units)

def test_get_weather_emoji(weather_provider):
    weather_code = "01d"
    expected_emoji = "☀️"
    assert weather_provider.get_weather_emoji(weather_code) == expected_emoji

def test_get_weather_cached(cached_weather_provider, mocker):
    location = "Berlin"
    units = "metric"
    cache_key = "cached_weather_Berlin_metric"
    expected_weather_data = {"temperature": 20, "humidity": 80}

    mocker.patch.object(CachedWeatherProviderBase, "fetch_weather_data", return_value=expected_weather_data)
    mocker.patch.object(CachedWeatherProviderBase, "get_cached_data", return_value=None)
    mocker.patch.object(CachedWeatherProviderBase, "cache_data")

    weather_data = cached_weather_provider.get_weather(location, units)

    CachedWeatherProviderBase.fetch_weather_data.assert_called_once_with(location, units=units)
    CachedWeatherProviderBase.get_cached_data.assert_called_once_with(cache_key)
    CachedWeatherProviderBase.cache_data.assert_called_once_with(cache_key, expected_weather_data, timeout=CachedWeatherProviderBase.CACHE_TIMEOUT)
    assert weather_data == expected_weather_data