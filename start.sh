#£¡/bin/bash
# Prepare for django
python3 manage.py migrate

# Start Uwsgi
uwsgi --ini uwsgi.ini