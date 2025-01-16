// Fetch guesthouses and populate the dropdown
async function loadGuesthouses() {
    try {
        const response = await fetch('/guesthouses'); // Update with the correct endpoint to fetch guesthouses
        if (!response.ok) {
            throw new Error('Failed to load guesthouses');
        }
        const guesthouses = await response.json();
        const guesthouseSelect = document.getElementById('guesthouseSelect');
        
        guesthouses.forEach(guesthouse => {
            const option = document.createElement('option');
            option.value = guesthouse.id;
            option.textContent = guesthouse.name;
            guesthouseSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading guesthouses:', error);
    }
}

// Fetch weather data when the user clicks the button
async function submitFormData() {
    const guesthouseSelect = document.getElementById('guesthouseSelect');
    const dateInput = document.getElementById('date');
    const guesthouseId = guesthouseSelect.value;
    const selectedDate = dateInput.value;

    if (!guesthouseId || !selectedDate) {
        alert('Please select a guesthouse and date.');
        return;
    }

    try {
        const response = await fetch(`/guesthouses/${guesthouseId}/weather/${selectedDate}`);
        if (!response.ok) {
            throw new Error('Failed to fetch weather data');
        }
        const data = await response.json();
        displayWeatherData(data);
    } catch (error) {
        console.error('Error fetching weather data:', error);
        alert('Error fetching weather data. Please try again.');
    }
}

// Display fetched data on the frontend
function displayWeatherData(data) {
    const weatherDataDiv = document.getElementById('weatherData');
    const alternativeDatesDiv = document.getElementById('alternativeDates');
    const suggestedGuesthousesDiv = document.getElementById('suggestedGuesthouses');

    // Clear previous content
    weatherDataDiv.innerHTML = '';
    alternativeDatesDiv.innerHTML = '';
    suggestedGuesthousesDiv.innerHTML = '';

    // Display weather forecast
    if (data.weather_forecast) {
        const forecastList = data.weather_forecast.map(forecast => `
            <p>${forecast.forecasted_date} at ${forecast.forecasted_time}: ${forecast.weather}</p>
        `).join('');
        weatherDataDiv.innerHTML = `<h3>Weather Forecast:</h3>${forecastList}`;
    }

    // Display alternative dates
    if (data.alternative_dates && data.alternative_dates !== "No better days found.") {
        const alternativeList = data.alternative_dates.map(date => `
            <p>${date.date} at ${date.forecasted_time}: ${date.weather}</p>
        `).join('');
        alternativeDatesDiv.innerHTML = `<h3>Alternative Dates:</h3>${alternativeList}`;
    } else {
        alternativeDatesDiv.innerHTML = `<h3>Alternative Dates:</h3><p>${data.alternative_dates}</p>`;
    }

    // Display suggested guesthouses
    if (data.suggested_guesthouses && data.suggested_guesthouses !== "No better options available.") {
        const suggestedList = data.suggested_guesthouses.map(guesthouse => `
            <div>
                <h4>${guesthouse.name} (${guesthouse.city})</h4>
                <p>Weather: ${guesthouse.weather}</p>
                <p>Amenities: ${guesthouse.amenities}</p>
                <p>Nearby Places: ${guesthouse['places nearby']}</p>
                <p>Restaurants/Cafes: ${guesthouse['restaurants and cafes nearby']}</p>
                <p>Airports Nearby: ${guesthouse['airports nearby']}</p>
            </div>
        `).join('');
        suggestedGuesthousesDiv.innerHTML = `<h3>Suggested Guesthouses:</h3>${suggestedList}`;
    } else {
        suggestedGuesthousesDiv.innerHTML = `<h3>Suggested Guesthouses:</h3><p>${data.suggested_guesthouses}</p>`;
    }
}

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
    loadGuesthouses();
});
