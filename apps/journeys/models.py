from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.timezone import timedelta


class Country(models.Model):
    code = models.CharField(
        max_length=2,
        help_text='ISO 3166-1 alpha-2 code',
        unique=True,
        validators=[
            RegexValidator(
                regex='^[A-Z]{2}$',
                message='Country code must be 2 characters long and uppercase',
            )
        ]
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.code} - {self.name}'

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super().save(*args, **kwargs)


class City(models.Model):
    code = models.CharField(
        max_length=3,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[A-Z]{3}$',
                message='City code must be 3 characters long and uppercase',
            )
        ]
    )
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.code} - {self.country.code} - {self.name}'

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super().save(*args, **kwargs)


class Flight(models.Model):
    number = models.CharField(
        max_length=6,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{2}\d{4}$',
                message='Flight number must be 2 uppercase letters followed by 4 digits',
            )
        ]
    )

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        self.number = self.number.upper()
        super().save(*args, **kwargs)


class FlightEvent(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    departure_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='departure_city')
    arrival_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='arrival_city')

    def __str__(self):
        return f'{self.flight.number} - {self.departure_city.code} - {self.arrival_city.code}'

    def get_duration(self):
        return self.arrival_time - self.departure_time

    def clean(self):
        if self.departure_time > self.arrival_time:
            raise ValidationError('Departure time cannot be later than arrival time.')

        if self.get_duration() == timedelta(seconds=0):
            raise ValidationError('Flight duration cannot be zero.')

        if self.get_duration() > timedelta(hours=24):
            raise ValidationError('Flight duration cannot exceed 24 hours.')
