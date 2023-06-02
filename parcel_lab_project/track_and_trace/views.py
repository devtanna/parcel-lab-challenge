from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django_ratelimit.decorators import ratelimit
from django.conf import settings

from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import Shipment
from .serializers import ShipmentDetailRequestSerializer
from .services.weather.open_weather_map import OpenWeatherMapProvider


class ShipmentDetailsView(viewsets.ViewSet):
    model = Shipment
    serializer_class = ShipmentDetailRequestSerializer
    weather_provider = OpenWeatherMapProvider

    @method_decorator(ratelimit(key=settings.RATE_LIMITER_KEY, rate=settings.RATE_LIMITER_RATE, method='GET'), name='shipment_retrieve')
    def retrieve(self, request, pk=None) -> Response:
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        tracking_number = serializer.validated_data['tracking_number']
        carrier = serializer.validated_data['carrier']
        weather_units = serializer.validated_data.get("weather_units", "metric")

        shipments = self.model.objects.filter(
            tracking_number=tracking_number,
            carrier__name__iexact=carrier
        )

        if not shipments:
            raise NotFound(_('Shipment not found.'))

        shipment_details = []
        for shipment in shipments:
            weather_data = {}
            if shipment.receiver_address.address:
                weather_data = self.weather_provider.get_weather(
                    location=shipment.receiver_address.address,
                    units=weather_units
                )
            
            shipment_details.append({
                'tracking_number': shipment.tracking_number,
                'carrier': shipment.carrier.name,
                'sender_address': shipment.sender_address.address,
                'receiver_address': shipment.receiver_address.address,
                'article': shipment.article.name,
                'quantity': shipment.article.quantity,
                'price': shipment.article.price,
                'sku': shipment.article.sku,
                'weather': weather_data,                
            })

        return Response({"shipments": shipment_details}, status=status.HTTP_200_OK)
