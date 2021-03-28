#!/bin/sh

django-admin migrate --noinput

if [ "${DEBUG:-}" = True ]; then
	exec django-admin runserver 0.0.0.0:8000
else
	django-admin collectstatic --noinput
	exec gunicorn ddnsbroker.wsgi:application --bind 0.0.0.0:8000
fi
