#!/usr/bin/env bash
# exit on error
set -o errexit


pip install -r requirements.txt


python manage.py migrate

# ESTA LÍNEA ES LA NUEVA: Carga los datos de la carpeta fixtures
python manage.py loaddata fixtures/datos.json

python manage.py collectstatic --noinput
