ruff check .
isort .

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Parcel Lab Project

## Project Setup

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

4. Database Migration & fixures
    ```shell
    python manage.py migrate
    python manage.py seed_shipments track_and_trace/fixtures/seed.csv
    ```
5. Set `OPEN_WEATHER_API_KEY` and `OPENCAGE_API_KEY` api keys in `local_settings.py` using the provided `local_settings.template`

5. Run the Development Server
    ```shell    
    python manage.py runserver
    ```
    The server will start running on http://127.0.0.1:8000/.

## Usage
```shell
curl http://127.0.0.1:8000/api/shipment-details/?tracking_number=TN12345682&carrier=gls&weather_units=metric | json_pp
```
- The endpoint is rate limited to `1000 requests / h` per `ip` which can be configured in settings. 


## Development Workflow
### Code Quality Checks
To perform code quality checks, run the following commands:

*Ruff*: An extremely fast Python linter, written in Rust.
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