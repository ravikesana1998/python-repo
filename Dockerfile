# Use official Python image as base
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . /app
COPY .env /app/.env

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt

# Expose the application port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
