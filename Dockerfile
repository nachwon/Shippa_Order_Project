FROM nachwon/shippa_order_base:latest

WORKDIR     /srv/app
COPY        . /srv/app

ENV         LANG C.UTF-8
ENV         DJANGO_SETTINGS_MODULE config.settings.prod

RUN         pyenv local app
RUN         /root/.pyenv/versions/app/bin/pip install -r /srv/app/requirements.txt

# Nginx setup
RUN         cp /srv/app/.deploy_settings/nginx/nginx.conf /etc/nginx/
RUN         cp /srv/app/.deploy_settings/nginx/shippa_order.conf /etc/nginx/sites-available/
RUN         rm -rf /etc/nginx/sites-enabled/*
RUN         ln -sf /etc/nginx/sites-available/shippa_order.conf /etc/nginx/sites-enabled/

# Log dir
RUN         mkdir -p /var/log/uwsgi/app

# manage.py
RUN         /root/.pyenv/versions/app/bin/python /srv/app/shippa_order/manage.py collectstatic --noinput
#RUN         /root/.pyenv/versions/app/bin/python /srv/app/shippa_order/manage.py migrate --noinput

# supervisor
RUN         cp /srv/app/.deploy_settings/supervisor/* /etc/supervisor/conf.d/
CMD         supervisord -n

# port
EXPOSE      80