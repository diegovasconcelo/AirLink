from datetime import datetime

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status

from apps.journeys.models import FlightEvent
from apps.journeys.serializers import FlightEventModelSerializer


class TestJourneyAPIView:
    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def setup_data(self, basic_flight_data):
        """Crea datos de prueba para los tests."""
        city_1 = basic_flight_data['city_1']
        city_2 = basic_flight_data['city_2']
        flight = basic_flight_data['flight']
        flight_event = FlightEvent.objects.create(
            flight=basic_flight_data['flight'],
            departure_time=timezone.make_aware(
                datetime(2025, 3, 3, 10, 0, 0)
            ),
            arrival_time=timezone.make_aware(
                datetime(2025, 3, 3, 14, 0, 0),
            ),
            departure_city=city_1,
            arrival_city=city_2
        )
        return {
            'flight_event': flight_event,
            'city1': city_1,
            'city2': city_2,
            'flight': flight
        }

    @pytest.mark.django_db
    def test_get_flight_events_without_params(self, client, setup_data):
        # Should return all FlightEvent objects if no parameters are passed.
        url = reverse('journey-search')
        response = client.get(url)
        flight_events = FlightEvent.objects.all()
        serializer = FlightEventModelSerializer(flight_events, many=True)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == serializer.data

    @pytest.mark.django_db
    def test_get_journeys_with_valid_params(self, client, setup_data):
        # Should call get_journeys and return journey data if valid parameters are passed.
        url = reverse('journey-search')
        params = {
            'date': '2025-03-03',
            'from': 'BUE',
            'to': 'MAD',
        }
        response = client.get(url, params)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_get_valid_journeys(self, client, setup_data):
        # Should return journey data if valid parameters are passed.
        url = reverse('journey-search')
        params = {
            'date': '2025-03-03',
            'from': 'BUE',
            'to': 'MAD',
        }
        response = client.get(url, params)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        first_journey = data[0]
        assert "connections" in first_journey
        assert "path" in first_journey
        assert isinstance(first_journey["path"], list)
        assert len(first_journey["path"]) > 0

        first_flight = first_journey["path"][0]
        expected_flight = {
            "flight_number": "AA1234",
            "from": "BUE",
            "to": "MAD",
            "departure_time": "2025-03-03 10:00",
            "arrival_time": "2025-03-03 14:00",
        }

        assert first_flight == expected_flight

    @pytest.mark.django_db
    def test_get_journeys_with_invalid_date(self, client, setup_data):
        # Should return a 400 error if the date is invalid.
        url = reverse('journey-search')
        params = {
            'date': 'invalid-date',
            'from': 'BUE',
            'to': 'MAD'
        }
        response = client.get(url, params)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.json()

    @pytest.mark.django_db
    def test_get_journeys_with_invalid_city(self, client, setup_data):
        # Should return a 400 error if any city is invalid.
        url = reverse('journey-search')
        params = {
            'date': '2025-03-03',
            'from': 'XYZ',  # This city does not exist
            'to': 'MAD'
        }
        response = client.get(url, params)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.json()

        # Also test with invalid destination city
        params = {
            'date': '2025-03-03',
            'from': 'BUE',
            'to': 'XYZ'  # This city does not exist
        }
        response = client.get(url, params)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.json()

    @pytest.mark.django_db
    def test_get_journeys_with_max_wait_time(self, client, setup_data):
        # Should accept the max_wait_time_hours parameter as a string.
        url = reverse('journey-search')
        params = {
            'date': '2025-03-03',
            'from': 'BUE',
            'to': 'MAD',
            'max_wait_time_hours': '5'
        }
        response = client.get(url, params)
        assert response.status_code == status.HTTP_200_OK
