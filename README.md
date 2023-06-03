# Parcel Lab Project

## Project setup using manage.py - See below for Docker setup

1. Clone the repository:
    ```shell
    git clone <repository-url>
    ```

2. Install the required dependencies:
    ``` shell
    pip install -r requirements.txt
    ```

3. Install the development dependencies if needed:
    ``` shell
    pip install -r requirements-dev.txt
    ```

4. Navigate to project folder
    ```shell
    cd parcel_lab_project
    ```

5. Database Migration & fixures
    ```shell
    python manage.py migrate
    python manage.py seed_shipments track_and_trace/fixtures/seed.csv
    ```
6. Set `OPEN_WEATHER_API_KEY` and `OPENCAGE_API_KEY` api keys in `local_settings.py` using the provided `local_settings.template`

7. Run the Development Server
    ```shell    
    python manage.py runserver
    ```
    The server will start running on http://127.0.0.1:8000/.

## Project setup using Docker
1. Clone the repository:
    ```shell
    git clone <repository-url>
    ```

2. Set `OPEN_WEATHER_API_KEY` and `OPENCAGE_API_KEY` api keys in `local_settings.py` using the provided `local_settings.template`

3. Build it:
    ``` shell
    docker build -t parcellab-challenge .
    ```

4. Run it:
    ``` shell
    docker run -p 8000:8000 parcellab-challenge
    ```

## Usage
```shell
curl http://127.0.0.1:8000/api/track-shipment/?tracking_number=TN12345682&carrier=gls&weather_units=metric | json_pp
```
Notes:
- The endpoint is rate limited to `1000 requests / h` per `ip` which can be configured in settings.
- Allowed values for weather_units parameter (optional): `metric`, `imperial`, `standard`


## Development Workflow
### Code Quality Checks
To perform code quality checks, run the following commands:

*pytest*: Run tests.
``` shell
pytest
```

*ruff*: An extremely fast Python linter, written in Rust.
``` shell
ruff check .
```

*isort*: A Python utility / library to sort imports alphabetically, and automatically separated into sections and by type
```shell
isort .
```

*mypy*: Type checks
```shell
mypy .
```

## Language Support
For other languages change the `LANGUAGE_CODE` in `settings.py`.

**Note**: The translations have **not** been added to the *.po files yet.