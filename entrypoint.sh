#!/bin/sh
cd $WORKDIR
python manage.py collectstatic --noinput

gunicorn protejabrasil.wsgi --timeout 999999 -c gunicorn.conf.py