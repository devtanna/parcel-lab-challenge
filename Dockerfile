# Use the official Python base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code to the working directory
COPY . /code

# Change the working directory to the project directory
WORKDIR /code/parcel_lab_project

# Run database migrations
RUN python manage.py migrate

# Seed the database with initial data
RUN python manage.py seed_shipments track_and_trace/fixtures/seed.csv

# Expose the port on which the application will run
EXPOSE 8000

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=parcel_lab_project.settings

# Start the Gunicorn server
CMD ["gunicorn", "parcel_lab_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
