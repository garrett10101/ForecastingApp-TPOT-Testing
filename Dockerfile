FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /ForecastingApp

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY app ./app/
COPY models ./models/

EXPOSE 5578

# FIXME: This runs the development server only (not for prod/deploy)
ENTRYPOINT ["python3", "app/app.py"]