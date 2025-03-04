from django.urls import path

from apps.journeys.views import (
    JourneyAPIView,
)

urlpatterns = [
    path('search', JourneyAPIView.as_view(), name='journey-search'),
]
