FROM python:3.12.3-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DEFAULT_TIMEOUT=100

# Upgrade pip
RUN pip install --upgrade pip

# Copy the requirements file
COPY requirements.txt /app

# Install dependencies with retry mechanism and increased timeout
RUN pip install --retries 5 --timeout 60 -r requirements.txt

# Copy the rest of the application code
COPY . /app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
