import pytest
from django.utils.translation import gettext as _

from track_and_trace.serializers import ShipmentDetailRequestSerializer


@pytest.fixture
def serializer():
    return ShipmentDetailRequestSerializer

def test_valid_serializer(serializer):
    data = {
        'weather_units': 'imperial',
        'tracking_number': 'ABC123',
        'carrier': 'Carrier1',
    }
    serializer_instance = serializer(data=data)
    assert serializer_instance.is_valid()
    assert not serializer_instance.errors

def test_missing_required_fields(serializer):
    data = {
        'weather_units': 'imperial',
    }
    serializer_instance = serializer(data=data)
    assert serializer_instance.is_valid() is False
    assert 'tracking_number' in serializer_instance.errors
    assert 'carrier' in serializer_instance.errors

def test_blank_tracking_number(serializer):
    data = {
        'weather_units': 'imperial',
        'tracking_number': '',
        'carrier': 'Carrier1',
    }
    serializer_instance = serializer(data=data)
    assert serializer_instance.is_valid() is False
    assert 'tracking_number' in serializer_instance.errors
    assert serializer_instance.errors['tracking_number'][0] == _('Tracking number is required.')

def test_blank_carrier(serializer):
    data = {
        'weather_units': 'imperial',
        'tracking_number': 'ABC123',
        'carrier': '',
    }
    serializer_instance = serializer(data=data)
    assert serializer_instance.is_valid() is False
    assert 'carrier' in serializer_instance.errors
    assert serializer_instance.errors['carrier'][0] == _('Carrier is required.')

def test_invalid_tracking_number(serializer):
    data = {
        'weather_units': 'imperial',
        'tracking_number': '@#$%',
        'carrier': 'Carrier1',
    }
    serializer_instance = serializer(data=data)
    assert serializer_instance.is_valid() is False
    assert 'tracking_number' in serializer_instance.errors
    assert serializer_instance.errors['tracking_number'][0] == _('Tracking number can only contain alphanumeric characters.')

def test_invalid_carrier(serializer):
    data = {
        'weather_units': 'imperial',
        'tracking_number': 'ABC123',
        'carrier': '@#$%',
    }
    serializer_instance = serializer(data=data)
    assert serializer_instance.is_valid() is False
    assert 'carrier' in serializer_instance.errors
    assert serializer_instance.errors['carrier'][0] == _("Carrier cannot contain special characters like '@', '#', '$', or '%'")