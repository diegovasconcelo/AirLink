from django.core.exceptions import ValidationError

from datetime import datetime

from apps.journeys.models import City


def validate_date_format(date, format: str = '%Y-%m-%d'):
    try:
        datetime.strptime(date, format)
    except ValueError:
        raise ValidationError(f'Invalid date format. Should be {format}.')


def validate_city(city_code: str):
    city_code = city_code.upper()
    if not City.objects.filter(code=city_code).exists():
        raise ValidationError(f'City with code "{city_code}" does not exist.')
