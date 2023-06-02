from rest_framework.routers import DefaultRouter

from track_and_trace.views import ShipmentDetailsView

router = DefaultRouter()
router.register(r'api', ShipmentDetailsView, basename='track-shipment')
urlpatterns = router.urls