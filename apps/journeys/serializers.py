from rest_framework import serializers

from apps.journeys.models import FlightEvent


class FlightEventModelSerializer(serializers.ModelSerializer):
    flight_number = serializers.CharField(source='flight.number')
    # from is a reserved keyword in Python, so we use _from instead
    _from = serializers.CharField(source="departure_city.code")
    to = serializers.CharField(source="arrival_city.code")

    class Meta:
        model = FlightEvent
        fields = [
            'flight_number',
            '_from',
            'to',
            'departure_time',
            'arrival_time'
        ]
        extra_kwargs = {
            '_from': {
                'source': 'departure_city'
            },
            'to': {
                'source': 'arrival_city'
            }
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Change the key name from _from to from to align with the API response
        data['from'] = data.pop('_from')
        return data


class FlightEventSerializer(serializers.Serializer):
    flight_number = serializers.CharField()
    _from = serializers.CharField()
    to = serializers.CharField()
    arrival_time = serializers.DateTimeField()
    departure_time = serializers.DateTimeField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['from'] = data.pop('_from')
        return dict(sorted(data.items()))


class Journeys(serializers.Serializer):
    connections = serializers.IntegerField()
    path = serializers.ListField(child=FlightEventSerializer())
