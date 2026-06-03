# 🌤 Weather City Ranking App

A fullstack application that retrieves weather data for specific cities using the
Open-Meteo API and generates a ranked list of cities based on a weather scoring
algorithm. The default date range is yesterday, but users can specify custom start and
end dates.

---

## Overview

This project demonstrates a fullstack architecture with:

- FastAPI backend for data processing and API handling
- Open-Meteo API for weather data
- Vanilla HTML, CSS, and JavaScript frontend
- Docker support for containerized deployment

Users can input a list of cities and a date range, and the system will:

1. Fetch hourly weather data for each city
2. Compute a weather score using a weighted algorithm
3. Return a ranked list of cities

---

## Weather Scoring Logic

Each city is evaluated using four weather parameters:

- Temperature (35% weight)
- Wind speed (20% weight)
- Relative humidity (20% weight)
- Cloud cover (25% weight)

### Ideal conditions:

- Temperature: 24°C
- Wind speed: 0
- Relative humidity: 50%
- Cloud cover: 25%

Each metric is converted into a score from 0 to 10 based on deviation from its ideal value. The final score is a weighted average of all components.

---

## Backend

The backend is built with FastAPI and exposes a REST API for ranking cities based on weather conditions.

To run locally:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
Once the backend is running, the API becomes available at:
```

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

The `/docs` endpoint provides an interactive Swagger interface where you can test all available API endpoints directly from the browser.

---

## Frontend

The frontend is built using plain HTML, CSS, and JavaScript. It provides a simple interface for interacting with the system by allowing users to:

- Enter a list of cities
- Select a date range
- View ranked results based on weather conditions

The frontend communicates with the backend through REST API calls and dynamically renders the ranking results.

---

## Docker Deployment

The entire application can be run using Docker Compose:

```bash
docker compose up --build
```

This command builds and starts both the backend and frontend services automatically. Once running, the system is fully accessible without requiring any manual setup.

After the containers start successfully, you can access the application through the frontend interface in your browser. The frontend communicates directly with the backend API to fetch weather data, compute scores, and display the ranked list of cities.

---

## API Endpoint

### Rank Cities

```http
POST /api/rank-cities
```
