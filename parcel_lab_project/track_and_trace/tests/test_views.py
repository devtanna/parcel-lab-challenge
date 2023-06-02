from decimal import Decimal
from unittest.mock import patch

import pytest
from django.shortcuts import resolve_url
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.test import APIRequestFactory

from track_and_trace.models import Address, Article, Carrier, Shipment
from track_and_trace.views import ShipmentDetailsView


@pytest.fixture
def shipment_details_view():
    return ShipmentDetailsView()


@pytest.fixture
def shipment_factory(db):
    def create_shipment(tracking_number, carrier, receiver_address, sender_address, article_name):
        shipment = Shipment.objects.create(
            tracking_number=tracking_number,
            carrier=Carrier.objects.create(name=carrier),
            receiver_address=Address.objects.create(address=receiver_address),
            sender_address=Address.objects.create(address=sender_address),
            article=Article.objects.create(
                name=article_name,
                quantity=1,
                price='10',
            ),
        )
        return shipment

    return create_shipment


def test_retrieve_valid_shipment(shipment_details_view, shipment_factory):
    factory = APIRequestFactory()
    request = factory.get(resolve_url("api/track-shipment"))

    # Create test data
    sender_address = Address.objects.create(address="Test Address 2")
    receiver_address = Address.objects.create(address="Test Address 1")
    shipment = shipment_factory(
        "12345", 
        "Test Carrier", 
        receiver_address, 
        sender_address, 
        "Test Article"
    )

    # Set up the request data
    request.query_params = {
        "tracking_number": "12345",
        "carrier": "Test Carrier",
        "weather_units": "metric",
    }

    weather_data = {
        'weather_emoji': '☀️',
        'temp': 25,
        'feels_like': 28,
        'temp_min': 20,
        'temp_max': 30,
    }
    with patch('track_and_trace.services.weather.open_weather_map.OpenWeatherMapProvider.get_weather', return_value=weather_data):
        # Call the retrieve method
        response = shipment_details_view.retrieve(request)

    # Check the response status code and data
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "shipments": [
            {
                "tracking_number": shipment.tracking_number,
                "carrier": shipment.carrier.name,
                "receiver_address": str(shipment.receiver_address),
                "sender_address": str(shipment.sender_address),
                "article": shipment.article.name,
                "quantity": shipment.article.quantity,
                "price": Decimal(shipment.article.price),
                "sku": shipment.article.sku,
                "weather": {
                    "weather_emoji": weather_data["weather_emoji"],
                    "temp": weather_data["temp"],
                    "feels_like": weather_data["feels_like"],
                    "temp_min": weather_data["temp_min"],
                    "temp_max": weather_data["temp_max"],
                },
            }
        ]
    }


@pytest.mark.django_db
def test_retrieve_invalid_shipment(shipment_details_view):
    factory = APIRequestFactory()
    request = factory.get(resolve_url("api/track-shipment"))

    # Set up the request data for an invalid shipment
    request.query_params = {
        "tracking_number": "99999",
        "carrier": "Invalid Carrier",
        "weather_units": "metric",
    }

    # Call the retrieve method and expect NotFound exception
    with pytest.raises(NotFound):
        shipment_details_view.retrieve(request)

@pytest.mark.django_db
def test_retrieve_without_carrier(shipment_details_view):
    factory = APIRequestFactory()
    request = factory.get(resolve_url("api/track-shipment"))

    # Set up the request data for an invalid shipment
    request.query_params = {
        "tracking_number": "99999",
        "weather_units": "metric",
    }

    # Call the retrieve method and expect ValidationError exception
    with pytest.raises(ValidationError):
        shipment_details_view.retrieve(request)


@pytest.mark.django_db
def test_retrieve_without_tracking_number(shipment_details_view):
    factory = APIRequestFactory()
    request = factory.get(resolve_url("api/track-shipment"))

    # Set up the request data for an invalid shipment
    request.query_params = {
        "carrier": "Invalid Carrier",
        "weather_units": "metric",
    }

    # Call the retrieve method and expect ValidationError exception
    with pytest.raises(ValidationError):
        shipment_details_view.retrieve(request)


@pytest.mark.django_db
def test_retrieve_without_tracking_number_and_carrier(shipment_details_view):
    factory = APIRequestFactory()
    request = factory.get(resolve_url("api/track-shipment"))

    # Set up the request data for an invalid shipment
    request.query_params = {
        "weather_units": "metric",
    }

    # Call the retrieve method and expect ValidationError exception
    with pytest.raises(ValidationError):
        shipment_details_view.retrieve(request)
