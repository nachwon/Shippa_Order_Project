FROM python:3.7.1
MAINTAINER nachwon@gmail.com

ENV         LANG C.UTF-8
ENV         DJANGO_SETTINGS_MODULE config.settings.prod

WORKDIR     /srv/app
COPY        . /srv/app

# APT Update
RUN         apt-get -y update
RUN         apt-get -y dist-upgrade

# Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# uWGSI install
RUN         pip install uwsgi

# Nginx install
RUN         apt-get -y install nginx
RUN         cp /srv/app/.deploy_settings/nginx/nginx.conf /etc/nginx/
RUN         cp /srv/app/.deploy_settings/nginx/shippa_order.conf /etc/nginx/sites-available/
RUN         rm -rf /etc/nginx/sites-enabled/*
RUN         ln -sf /etc/nginx/sites-available/shippa_order.conf /etc/nginx/sites-enabled/

# supervisor install
RUN         apt-get -y install supervisor

# Log dir
RUN         mkdir -p /var/log/uwsgi/app

# manage.py
WORKDIR     /srv/app/soundhub
RUN         /root/.pyenv/versions/app/bin/python /srv/app/soundhub/manage.py collectstatic --noinput
RUN         /root/.pyenv/versions/app/bin/python /srv/app/soundhub/manage.py migrate --noinput

# supervisor
RUN         cp /srv/app/.config/supervisor/* /etc/supervisor/conf.d/
CMD         supervisord -n

# port
EXPOSE      80