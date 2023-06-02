from django.utils.translation import gettext as _
from rest_framework import serializers

TRACKING_NUMBER_MIN_LENGTH = 3
TRACKING_NUMBER_MAX_LENGTH = 32
CARRIER_MIN_LENGTH = 3
CARRIER_MAX_LENGTH = 32

class ShipmentDetailRequestSerializer(serializers.Serializer):
    weather_units = serializers.ChoiceField(
        choices=['imperial', 'standard', 'metric'],
        required=False
    )
    tracking_number = serializers.CharField(
        min_length=TRACKING_NUMBER_MIN_LENGTH,
        max_length=TRACKING_NUMBER_MAX_LENGTH,
        allow_blank=False,
        allow_null=False,
        error_messages={
            'min_length': _(f'Tracking number must be at least {TRACKING_NUMBER_MIN_LENGTH} characters long.'),
            'max_length': _(f'Tracking number cannot exceed {TRACKING_NUMBER_MAX_LENGTH} characters.'),
            'blank': _('Tracking number is required.'),
            'null': _('Tracking number is required.'),
        }
    )
    carrier = serializers.CharField(
        min_length=CARRIER_MIN_LENGTH,
        max_length=CARRIER_MAX_LENGTH,
        allow_blank=False,
        allow_null=False,
        error_messages={
            'min_length': _(f'Carrier must be at least {CARRIER_MIN_LENGTH} characters long.'),
            'max_length': _(f'Carrier cannot exceed {CARRIER_MAX_LENGTH} characters.'),
            'blank': _('Carrier is required.'),
            'null': _('Carrier is required.'),
        }
    )

    def validate_tracking_number(self, value) -> str:
        if not value.isalnum():
            raise serializers.ValidationError(_('Tracking number can only contain alphanumeric characters.'))
        return value

    def validate_carrier(self, value):
        if any(char in value for char in ['@', '#', '$', '%']):
            raise serializers.ValidationError("Carrier cannot contain special characters like '@', '#', '$', or '%'")
        return value
