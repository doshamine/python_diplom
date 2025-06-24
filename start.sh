#!/bin/bash

python3 manage.py makemigrations
python3 manage.py migrate --noinput
echo "from django.contrib.auth.models import User; \
User.objects.filter(username='admin').exists() or \
User.objects.create_superuser('admin', 'admin@example.com', '123')" | python3 manage.py shell
python3 manage.py import
python3 manage.py runserver 0.0.0.0:8000
