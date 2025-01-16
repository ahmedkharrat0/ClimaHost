# Guesthouse Weather Forecast

This project provides an API for fetching weather forecasts for guesthouses in Tunisia. It allows users to get weather data for specific guesthouses based on a selected date, with features to suggest alternative dates and guesthouses based on weather conditions. The application uses FastAPI for the backend and integrates with weather API "7timer" to provide up-to-date weather data.

## Features

- **Weather Forecast**: Get weather data for a specific guesthouse on a chosen date.
- **Alternative Dates**: If the weather on the selected date is undesirable, find alternative dates with better weather for the same guesthouse.
- **Suggested Guesthouses**: Get suggestions for other guesthouses with good weather on the selected date.
- **Guesthouse Management**: Admin users can manage guesthouse data via an authentication system.

## Technologies Used

- **Backend**: FastAPI
- **Database**: SQLite
- **Weather API**: Integrated with a public weather API to fetch weather data for guesthouses.
- **Authentication**: OAuth 2.0 and JWT for secure login and admin access.
- **Frontend**: HTML, CSS, and JavaScript (using `fetch` API to interact with the backend).
- **Docker**: The project is containerized using Docker for easy deployment.

## Installation

### Prerequisites

- Python 3.8 or higher
- Docker (optional, for containerized deployment)

### Steps to Run the Project Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/guesthouse-weather-forecast.git
   cd guesthouse-weather-forecast
