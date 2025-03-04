from datetime import timedelta, datetime

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.journeys.models import FlightEvent, Country, City, Flight


class TestCountry:
    @pytest.mark.django_db
    def test_country_creation(self):
        country = Country.objects.create(code='ES', name='Spain')
        assert country.code == 'ES'
        assert country.name == 'Spain'

    @pytest.mark.django_db
    def test_country_code_unique(self):
        Country.objects.create(code='FR', name='France')
        with pytest.raises(Exception):
            Country.objects.create(code='FR', name='Another France')


class TestCity:
    @pytest.mark.django_db
    def test_city_creation(self, basic_flight_data):
        # Should create a city with the given data.
        country = basic_flight_data['country_2']
        city = City.objects.create(code='BCN', name='Barcelona', country=country)
        assert city.code == 'BCN'
        assert city.name == 'Barcelona'
        assert city.country == country

    @pytest.mark.django_db
    def test_city_code_unique(self, basic_flight_data):
        # Should raise an exception if a city with the same code already exists.
        country = basic_flight_data['country_1']
        City.objects.create(code='CBA', name='Córdoba', country=country)
        with pytest.raises(Exception):
            City.objects.create(code='CBA', name='Another Córdoba', country=country)


class TestFlight:
    @pytest.mark.django_db
    def test_flight_creation(self):
        # Should create a flight with the given data and uppercase the flight number.
        flight = Flight.objects.create(number='aa1234')
        assert flight.number == 'AA1234'

    @pytest.mark.django_db
    def test_flight_number_unique(self):
        # Should raise an exception if a flight with the same number already exists.
        Flight.objects.create(number='AA1234')
        with pytest.raises(Exception):
            Flight.objects.create(number='AA1234')


class TestFlightEvent:
    @pytest.mark.django_db
    def test_flight_event_creation(self, basic_flight_data):
        # Should create a flight event with the given data.
        flight_event = FlightEvent.objects.create(
            flight=basic_flight_data['flight'],
            departure_time=timezone.make_aware(
                datetime(2025, 3, 3, 10, 0, 0)
            ),
            arrival_time=timezone.make_aware(
                datetime(2025, 3, 3, 14, 0, 0)
            ),
            departure_city=basic_flight_data['city_1'],
            arrival_city=basic_flight_data['city_2']
        )
        assert flight_event.flight == basic_flight_data['flight']
        assert flight_event.departure_city == basic_flight_data['city_1']
        assert flight_event.arrival_city == basic_flight_data['city_2']

    @pytest.mark.django_db
    def test_flight_event_duration(self, basic_flight_data):
        # Should return the duration of the flight event as a timedelta object.
        flight_event = FlightEvent.objects.create(
            flight=basic_flight_data['flight'],
            departure_time=timezone.make_aware(
                datetime(2025, 3, 3, 10, 0, 0)
            ),
            arrival_time=timezone.make_aware(
                datetime(2025, 3, 3, 14, 0, 0)
            ),
            departure_city=basic_flight_data['city_1'],
            arrival_city=basic_flight_data['city_2']
        )
        assert flight_event.get_duration() == timedelta(hours=4)

    @pytest.mark.django_db
    def test_flight_event_invalid_times(self, basic_flight_data):
        # Should raise a ValidationError if the departure time is later than the arrival time.
        flight_event = FlightEvent(
            flight=basic_flight_data['flight'],
            departure_time=timezone.make_aware(
                datetime(2025, 3, 3, 10, 0, 0)
            ),
            arrival_time=timezone.make_aware(
                datetime(2025, 3, 3, 9, 0, 0)
            ),
            departure_city=basic_flight_data['city_1'],
            arrival_city=basic_flight_data['city_2']
        )
        with pytest.raises(ValidationError) as e:
            flight_event.clean()
        assert 'Departure time cannot be later than arrival time.' in str(e.value)

    @pytest.mark.django_db
    def test_flight_event_duration_exceeds_limit(self, basic_flight_data):
        # Should raise a ValidationError if the flight duration exceeds 24 hours.
        flight_event = FlightEvent(
            flight=basic_flight_data['flight'],
            departure_time=timezone.make_aware(
                datetime(2025, 3, 3, 10, 0, 0)
            ),
            arrival_time=timezone.make_aware(
                datetime(2025, 3, 4, 22, 10, 0)
            ),
            departure_city=basic_flight_data['city_1'],
            arrival_city=basic_flight_data['city_2']
        )
        with pytest.raises(ValidationError) as e:
            flight_event.clean()
        assert 'Flight duration cannot exceed 24 hours.' in str(e.value)

    @pytest.mark.django_db
    def test_flight_event_zero_duration(self, basic_flight_data):
        # A flight with the same departure and arrival time should not be allowed.
        flight_event = FlightEvent(
            flight=basic_flight_data['flight'],
            departure_time=timezone.make_aware(
                datetime(2025, 3, 3, 10, 0, 0)
            ),
            arrival_time=timezone.make_aware(
                datetime(2025, 3, 3, 10, 0, 0)
            ),
            departure_city=basic_flight_data['city_1'],
            arrival_city=basic_flight_data['city_2']
        )
        with pytest.raises(ValidationError, match='Flight duration cannot be zero.'):
            flight_event.clean()

    @pytest.mark.django_db
    def test_flight_event_exactly_24_hours(self, basic_flight_data):
        # A flight that lasts exactly 24 hours should be valid.
        flight_event = FlightEvent(
            flight=basic_flight_data['flight'],
            departure_time=timezone.make_aware(
                datetime(2025, 3, 3, 10, 0, 0)
            ),
            arrival_time=timezone.make_aware(
                datetime(2025, 3, 4, 10, 0, 0)
            ),
            departure_city=basic_flight_data['city_1'],
            arrival_city=basic_flight_data['city_2']
        )
        flight_event.clean()
