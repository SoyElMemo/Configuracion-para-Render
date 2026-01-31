#!/usr/bin/env bash

set -o errexit

# Instalar librerías
pip install -r requirements.txt

# Recolectar archivos estáticos (CSS/JS)
python manage.py collectstatic --noinput

# Migrar la base de datos
python manage.py migrate

# Cargar los datos limpios (sin logs ni basura)
python manage.py loaddata fixtures/datos.json