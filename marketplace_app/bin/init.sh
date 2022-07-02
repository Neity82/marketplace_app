#!/bin/sh

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py loaddata seo.json banners.json discount.json users.json shop.json product.json orders.json atribute.json