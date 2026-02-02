#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar librerías
pip install -r requirements.txt

# Recolectar archivos estáticos
# Quitamos --clear para evitar problemas de permisos en Render
python manage.py collectstatic --no-input

# Migraciones
python manage.py migrate