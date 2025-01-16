
# Guesthouse Weather Forecast

This project provides an API for fetching weather forecasts for guesthouses in Tunisia. It allows users to get weather data for specific guesthouses based on a selected date, with features to suggest alternative dates and guesthouses based on weather conditions. The application uses FastAPI for the backend and integrates with the "7timer" weather API to provide up-to-date weather data.

## Features

- **Weather Forecast**: Retrieve weather data for a specific guesthouse on a chosen date.
- **Alternative Dates**: Suggests other dates with better weather for the same guesthouse if the selected date's weather is undesirable.
- **Suggested Guesthouses**: Recommends other guesthouses with favorable weather on the selected date.
- **Guesthouse Management**: Admin users can manage guesthouse data through an authentication system.

## Technologies Used

- **Backend**: FastAPI
- **Database**: SQLite
- **Weather API**: Integration with the "7timer" public weather API for weather forecasts.
- **Authentication**: OAuth 2.0 and JWT for secure login and admin access.
- **Frontend**: HTML, CSS, and JavaScript (using the `fetch` API for backend interaction).
- **Docker**: The project is containerized with Docker for seamless deployment.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- Docker (optional, for containerized deployment)

---

### Steps to Run the Project Locally

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/guesthouse-weather-forecast.git
   cd guesthouse-weather-forecast
   ```

2. **Create a Virtual Environment** (Optional but Recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the API**:
   Open your browser and navigate to:
   - API Documentation: `http://127.0.0.1:8000/docs`
   - Root Endpoint: `http://127.0.0.1:8000`

---

### Steps to Run the Project with Docker

1. **Build and Start the Containers**:
   ```bash
   docker-compose build
   docker-compose up
   ```

2. **Access the API**:
   - API Documentation: `http://localhost:8000/docs`
   - Root Endpoint: `http://localhost:8000`

3. **Stop the Containers**:
   Press `Ctrl+C` to stop the running containers, then clean up:
   ```bash
   docker-compose down
   ```

---

## Usage

1. **Admin Features**:
   - Register as an admin to manage guesthouse data.
   - Use `/admin` endpoints for CRUD operations.

2. **Weather Recommendations**:
   - Use `/recommendations` to get weather suggestions based on a date and guesthouse ID.

3. **Public Access**:
   - Visitors can fetch weather and recommendations without needing to log in.
