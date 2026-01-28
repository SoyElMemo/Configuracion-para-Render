#!/usr/bin/env bash
# Script de build para Render.com

set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Hacer migraciones
python manage.py migrate

# Recopilar archivos estáticos
python manage.py collectstatic --noinput
