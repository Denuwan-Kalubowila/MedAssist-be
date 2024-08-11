FROM python:3.12.3-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DEFAULT_TIMEOUT=100

RUN pip install --upgrade pip

COPY requirements.txt /app

RUN pip install --retries 5 --timeout 60 -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
