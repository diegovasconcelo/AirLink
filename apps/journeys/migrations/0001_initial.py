# Generated by Django 5.1.6 on 2025-03-03 14:24

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='ISO 3166-1 alpha-2 code', max_length=2, unique=True, validators=[django.core.validators.RegexValidator(message='Country code must be 2 characters long and uppercase', regex='^[A-Z]{2}$')])),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=6, unique=True, validators=[django.core.validators.RegexValidator(message='Flight number must be 2 uppercase letters followed by 4 digits', regex='^[A-Z]{2}\\d{4}$')])),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, unique=True, validators=[django.core.validators.RegexValidator(message='City code must be 3 characters long and uppercase', regex='^[A-Z]{3}$')])),
                ('name', models.CharField(max_length=100)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journeys.country')),
            ],
        ),
        migrations.CreateModel(
            name='FlightEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
                ('arrival_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrival_city', to='journeys.city')),
                ('departure_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departure_city', to='journeys.city')),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journeys.flight')),
            ],
        ),
    ]
