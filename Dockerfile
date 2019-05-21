FROM python:3-alpine

# Install nginx and configuration
RUN apk add --no-cache nginx curl \
    && mkdir -p /run/nginx/
ADD docker/django.conf /etc/nginx/django.conf

# our python is in app
ENV PYTHONPATH /app

# Install Django App and setup the setting module
ADD MOI /app/MOI
ADD moiregistry /app/moiregistry
ADD usercore /app/usercore
ADD manage.py /app/manage.py
ADD requirements.txt /app/requirements.txt
ADD LICENSE /app/LICENSE

ENV DJANGO_SETTINGS_MODULE "MOI.docker_settings"

# /entrypoint.sh
ADD docker/entrypoint.sh /entrypoint.sh

# Add the entrypoint and add configuration
WORKDIR /app/

# Install python deps
RUN mkdir -p /var/www/static \
    && pip install -r requirements.txt \
    && pip install gunicorn==19.7

### ALL THE CONFIGURATION

# The secret key used for django
ENV DJANGO_SECRET_KEY ""

# A comma-seperated list of allowed hosts
ENV DJANGO_ALLOWED_HOSTS "localhost"

# Database settings
## Use SQLITE out of the box
ENV DJANGO_DB_ENGINE "django.db.backends.sqlite3"
ENV DJANGO_DB_NAME "/data/mhadmin.db"
ENV DJANGO_DB_USER ""
ENV DJANGO_DB_PASSWORD ""
ENV DJANGO_DB_HOST ""
ENV DJANGO_DB_PORT ""

# Volume and ports
VOLUME /data/
EXPOSE 80
HEALTHCHECK --start-period=10s CMD curl -f http://localhost/ || exit 1
ENTRYPOINT ["/entrypoint.sh"]