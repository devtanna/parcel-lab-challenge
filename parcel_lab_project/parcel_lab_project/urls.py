from django.urls import include, path

urlpatterns = [
    path("", include("track_and_trace.urls")),
]
