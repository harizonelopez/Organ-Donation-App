FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN DJANGO_SECRET_KEY=build-placeholder \
    DJANGO_DEBUG=False \
    python manage.py collectstatic --noinput
    
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
