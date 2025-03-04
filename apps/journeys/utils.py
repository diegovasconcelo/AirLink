from datetime import datetime, timedelta

from typing import List, Dict
from django.utils import timezone

from apps.journeys.models import FlightEvent


def parse_journey(journeys: List[List[FlightEvent]]) -> List[Dict]:
    """
        Parses the list of journeys to match the expected format by the frontend.
        ---
        Parameters:
            - journeys: List of journeys, where each journey is a list of flight events `FlightEvent`.

        Returns:
            A list of journeys, where each journey is a dictionary with the following structure:
            {
                "connections": int,
                "path": [
                    {
                        "flight_number": str,
                        "_from": str,
                        "to": str,
                        "departure_time": str,
                        "arrival_time": str
                    }
                ]
            }
    """
    parsed_journeys = []
    for journey in journeys:
        total_connections = 0 if len(journey) == 1 else len(journey)
        parsed_journeys.append({
            "connections": total_connections,
            "path": [
                {
                    "flight_number": flight_event.flight.number,
                    "_from": flight_event.departure_city.code,
                    "to": flight_event.arrival_city.code,
                    "departure_time": flight_event.departure_time.strftime('%Y-%m-%d %H:%M'),
                    "arrival_time": flight_event.arrival_time.strftime('%Y-%m-%d %H:%M')
                }
                for flight_event in journey
            ]
        })
    return parsed_journeys


def get_journeys(date: str, from_city: str, to_city: str, max_wait_time_hours: int) -> List[FlightEvent]:
    """
        Searches for "journeys" (sequences of 1 or 2 flight events) connecting
            an origin with a destination, departing on a given date.
        ---
        Parameters:
            - date: Departure date in 'YYYY-MM-DD' format
            - from_city: Origin city code (3 letters)
            - to_city: Destination city code (3 letters)
            - max_wait_time_hours: Max. connection time allowed between flights

        Returns:
            A list of journeys, where each journey is a list of `FlightEvent`.
    """
    # Data normalization
    start_date = timezone.make_aware(
        datetime.strptime(date, '%Y-%m-%d')
    )
    from_city = from_city.upper()
    to_city = to_city.upper()
    max_wait_time = timedelta(hours=int(max_wait_time_hours))
    journeys = []

    # 1. We look for all events departing on the given date from the origin city.
    initial_flights = FlightEvent.objects.filter(
        departure_time__date=start_date,
        departure_city__code=from_city
    )

    # 2. Direct flights: events going from origin to destination.
    direct_flights = initial_flights.filter(arrival_city__code=to_city)
    for flight in direct_flights:
        if flight.get_duration() <= timedelta(hours=24):
            journeys.append([flight])

    """
        3. Connecting flights: for each flight departing from 'from_city' and NOT going directly to the destination,
            we look for a second flight that meets the connection conditions.
        Direct flights are excluded to avoid duplicates.
    """
    connecting_flights = initial_flights.exclude(arrival_city__code=to_city)
    for flight1 in connecting_flights:
        """
            We look for flights where:
                - The second flight departs from the arrival city of the first flight.
                - The second flight arrives at the destination city.
                - The second flight departs after the arrival of the first one.
        """
        potential_connections = FlightEvent.objects.filter(
            departure_city=flight1.arrival_city,
            arrival_city__code=to_city,
            departure_time__gt=flight1.arrival_time,
        )
        for flight2 in potential_connections:
            wait_time = flight2.departure_time - flight1.arrival_time
            total_duration = flight2.arrival_time - flight1.departure_time
            if wait_time <= max_wait_time and total_duration <= timedelta(hours=24):
                journeys.append([flight1, flight2])
    # journeys = sorted(journeys, key=lambda journey: journey[0].departure_time)

    return parse_journey(journeys)
