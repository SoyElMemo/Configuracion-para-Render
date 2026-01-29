#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Recopilar estáticos primero
python manage.py collectstatic --noinput

# Aplicar migraciones
python manage.py migrate

# CARGAR DATOS (Agregamos --exclude para evitar el error de duplicados)
python manage.py loaddata fixtures/datos.json --exclude auth.permission --exclude contenttypes