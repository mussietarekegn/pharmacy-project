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

# 5. Print all users and their staff/superuser status (for verification)
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
for u in User.objects.all():
    print(f"Username: {u.username}, is_staff: {u.is_staff}, is_superuser: {u.is_superuser}")
EOF
