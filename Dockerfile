FROM python:3-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /ddnsbroker

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn psycopg2-binary

COPY container/settings.py container/run.sh src/ ./
ENV PYTHONPATH=.
ENV DJANGO_SETTINGS_MODULE=settings

VOLUME /ddnsbroker/static
VOLUME /ddnsbroker/var

CMD ["/bin/sh", "run.sh"]

EXPOSE 8000/tcp
