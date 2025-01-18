FROM python:3.9-slim

WORKDIR /guesthousesapi

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

COPY guesthouses.csv /app/guesthouses.csv


EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
