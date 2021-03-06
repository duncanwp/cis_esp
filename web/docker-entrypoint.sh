#!/bin/bash
# From http://michal.karzynski.pl/blog/2015/04/19/packaging-django-applications-as-docker-container-images/

# Wait for the DB to be up...
sleep 10

python manage.py migrate                  # Apply database migrations
if [ "$DEBUG" = "True" ]; then
  python manage.py loaddata test_fixtures.json  # Load in some test data
fi
python manage.py collectstatic --noinput  # Collect static files

# Prepare log files and start outputting logs to stdout
touch /cis-esp/logs/gunicorn.log
touch /cis-esp/logs/access.log
tail -n 0 -f /cis-esp/logs/*.log &

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn cis_esp.wsgi:application \
    --name cis_esp \
    --bind :8000 \
    --workers 3 \
    --log-level=info \
    --log-file=/cis-esp/logs/gunicorn.log \
    --access-logfile=/cis-esp/logs/access.log \
    "$@"