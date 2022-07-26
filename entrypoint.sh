#!/bin/bash
python manage.py migrate --noinput;
if [ "$ENV" != "heroku" ]; then
  python manage.py runserver 0.0.0.0:8000;
fi
if [ "$ENV" = "heroku" ]; then
  python manage.py collectstatic --noinput;
  gunicorn stock_market.wsgi:application --bind 0.0.0.0:$PORT --access-logfile -;
fi
