import pytest

from apps.journeys.models import Country, City, Flight


@pytest.fixture
def basic_flight_data(db):
    country_1 = Country.objects.create(code='AR', name='Argentina')
    country_2 = Country.objects.create(code='ES', name='Spain')
    city_1 = City.objects.create(code='BUE', name='Bueno Aires', country=country_1)
    city_2 = City.objects.create(code='MAD', name='Madrid', country=country_2)
    flight = Flight.objects.create(number='AA1234')

    return {
        'country_1': country_1,
        'country_2': country_2,
        'city_1': city_1,
        'city_2': city_2,
        'flight': flight,
    }
