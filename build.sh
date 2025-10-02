#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# One-time superuser creation (run once, then remove these lines)
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='Maikel').exists() or User.objects.create_superuser('admin', 'nwokikeonyeka@gmail.com', 'Maikel1@')" | python manage.py shell
