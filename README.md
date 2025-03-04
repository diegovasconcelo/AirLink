# AirLink ✈️

A simple API for searching flights, built with Django and Django REST Framework.


## ✨ Features
- Search for flights based on origin, destination, and date.
- Retrieve detailed flight information (e.g., flight number, departure time, arrival time).
- Deployable with Docker.

## Dependencies
* `Docker`
* `Make` (optional, used for running common commands)

## 🚀 Getting Started
### 1. Clone the repository
```bash
git clone https://github.com/diegovasconcelo/AirLink.git
```

### 2. Setup the environment
```bash
cd AirLink
cp .env.example .env
# Update the .env file with your own settings
```
### 3. Build the Docker image
> 💡 If you have `Make` installed, you can run the following commands with it. Otherwise, you can run the commands listed in the `Makefile` manually.

using Make:
```bash
make build
```

or manually with Docker:
```bash
docker build -t airlink .
```
### 4. Run the server
```bash
make run
```
or manually with Docker:
```bash
docker run --rm --env-file .env  -d -p 8000:8000 --name air-link air-link
```
### 5. Access the API
You can access the API at `http://localhost:8000/journeys/search`.

### 6. If you want to stop the server
```bash
make stop
```


## 📡 API Usage
> 🔗 The API is accessible at https://airlink.cloud.dvutech.io/journeys/search .
### 🔍 Search Flights

Endpoint: `GET` `/journeys/search`

> Returns a list of all available flights, to see the available flights.

Example Request

```bash
curl -X GET "https://airlink.cloud.dvutech.io/journeys/search"
```
Response
```json
[
    {
        "id": 15,
        "flight_number": "PA0309",
        "to": "SAO",
        "departure_time": "2025-03-04T05:00:00Z",
        "arrival_time": "2025-03-04T17:10:00Z",
        "from": "PAR"
    },
    {
        "id": 16,
        "flight_number": "SC2565",
        "to": "MIA",
        "departure_time": "2025-03-05T01:10:00Z",
        "arrival_time": "2025-03-05T10:50:00Z",
        "from": "SCL"
    }
]
```

Endpoint: `GET` `/journeys/search` (with query parameters)
> Returns a list of all available flights based on the query parameters.

* Query Parameters:
  - `date`: The date of the flight (format: `YYYY-MM-DD`).
  - `from`: The origin of the flight (e.g., `BUE`).
  - `to`: The destination of the flight (e.g., `MIL`).

Example Request
```bash
curl -X GET "https://airlink.cloud.dvutech.io/journeys/search?date=2025-03-05&from=bue&to=mil"
```
Response
```json
[
    {
        "connections": 0,
        "path": [
            {
                "arrival_time": "2025-03-06 07:28",
                "departure_time": "2025-03-05 07:30",
                "flight_number": "BU3547",
                "from": "BUE",
                "to": "MIL"
            }
        ]
    },
    {
        "connections": 2,
        "path": [
            {
                "arrival_time": "2025-03-05 01:45",
                "departure_time": "2025-03-05 01:00",
                "flight_number": "BU3510",
                "from": "BUE",
                "to": "MVD"
            },
            {
                "arrival_time": "2025-03-05 19:55",
                "departure_time": "2025-03-05 03:00",
                "flight_number": "MV8551",
                "from": "MVD",
                "to": "MIL"
            }
        ]
    }
]
```


### 📂 Project Structure
It includes the following (approach):
```plaintext
AirLink/
├── apps/
│   └── journeys/              # Main app for the project.
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── migrations/
│       ├── serializers.py
│       ├── urls.py
│       ├── utils.py
│       ├── validators.py
│       └── views.py
├── core/
│   ├── asgi.py
│   ├── settings.py            # Base settings for the project.
│   ├── urls.py
│   └── wsgi.py
├── data/
│   └── fixtures/
│       └── journeys/
│           └── data.json       # For loading initial data.
├── requirements/
│    ├── base.txt
│    ├── dev.txt
│    └── prod.txt
├── tests/
│   └── journeys/               # Simple test for the journeys app.
│       ├── conftest.py
│       ├── test_models.py
│       └── test_views.py
├── .dockerignore
├── .gitignore
├── .env                        # For storing environment variables.
├── .env.*.example              # Example of the .envs files
├── db.sqlite3                  # Only until the DB logic is finished.
├── Makefile                    # For running common commands (shortcuts).
├── Dockerfile
├── entrypoint.sh               # For running the server.
├── manage.py
├── captain-defition            # For deploying the app using CapRover (own PaaS).
├── pytest.ini                  # Configuration for pytest.
└── README.md
```
