from rest_framework.views import APIView
from rest_framework.response import Response

from apps.journeys.models import FlightEvent
from apps.journeys.serializers import FlightEventModelSerializer, Journeys
from apps.journeys.utils import get_journeys
from apps.journeys.validators import validate_date_format, validate_city


class JourneyAPIView(APIView):
    """
        Handles GET requests to retrieve journey information.
        ---
        Query Parameters:
        - date (str): The date of the journey in 'YYYY-MM-DD' format.
        - from (str): The departure city.
        - to (str): The destination city.
        - max_wait_time_hours (int, optional): The maximum wait time in hours. Defaults to 4.

        Returns:
        - Response: A JSON response containing journey data.

        If 'date', 'from', and 'to' parameters are provided and valid, it retrieves journeys
        based on the provided parameters. Otherwise, it retrieves all flight events for display.
    """

    def get(self, request):
        date = request.query_params.get('date')
        from_city = request.query_params.get('from')
        to_city = request.query_params.get('to')
        if date and from_city and to_city:
            try:
                validate_date_format(date)
                validate_city(from_city)
                validate_city(to_city)
            except Exception as e:
                return Response(
                    {
                        'error': e.message
                    }, status=400
                )
            max_wait_time_hours = request.query_params.get('max_wait_time_hours', 4)
            journeys = get_journeys(date, from_city, to_city, max_wait_time_hours)
            serializer = Journeys(journeys, many=True)
        else:
            flight_events = FlightEvent.objects.all()
            serializer = FlightEventModelSerializer(flight_events, many=True)
        return Response(serializer.data)
