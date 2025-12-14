#!/usr/bin/env bash
set -o errexit

# 1. Install dependencies
pip install -r requirements.txt

# 2. Collect static files
python manage.py collectstatic --noinput

# 3. Apply migrations
python manage.py migrate

# 4. Create superuser automatically if it doesn't exist
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='hp').exists():
    User.objects.create_superuser('hp', 'moss@gmail.com', 'Moss123@')
EOF
