#!/usr/bin/env bash
set -o errexit

# 1. Install dependencies
pip install -r requirements.txt

# 2. Collect static files
python manage.py collectstatic --noinput

# 3. Apply migrations
python manage.py migrate

# 4. Create superuser if it doesn't exist (force staff and superuser)
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='hp').exists():
    User.objects.create_superuser(username='hp', email='moss@gmail.com', password='mussie123456789012')
u = User.objects.get(username='hp')
u.is_staff = True
u.is_superuser = True
u.save()
print(f'Created/Updated superuser: {u.username}, is_staff={u.is_staff}, is_superuser={u.is_superuser}')
"
