#!/usr/bin/env bash

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate --noinput

# Seed database
python manage.py shell -c "from seed import seed_students; seed_students.create_staff_students(); seed_students.create_students()"

# Start Gunicorn server
gunicorn -b :8000 Bookflow.wsgi
