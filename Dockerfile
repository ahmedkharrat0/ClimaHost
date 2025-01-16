FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /guesthousesapi

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
#COPY . /app
#COPY . /static
# Copy the rest of the application code into the container
#COPY static /guesthousesapi/static
#COPY templates /guesthousesapi/templates
COPY . .

COPY guesthouses.csv /app/guesthouses.csv


# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
