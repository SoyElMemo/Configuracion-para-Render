# Instrucciones para Desplegar en Render.com

## Pasos para configurar tu aplicación Django en Render:

### 1. **Crea una cuenta en Render.com**
   - Ve a https://render.com
   - Crea una cuenta con GitHub

### 2. **Conecta tu repositorio GitHub**
   - En Render, haz clic en "New" > "Web Service"
   - Selecciona "Build and deploy from a Git repository"
   - Autoriza a Render para acceder a tu GitHub
   - Selecciona el repositorio `Configuracion-para-Render`

### 3. **Configura las variables de entorno en Render**

En el dashboard de Render, ve a tu servicio y en la sección **Environment Variables**, añade:

```
DATABASE_URL=postgresql://[usuario]:[contraseña]@[host]:[puerto]/[base_datos]
SECRET_KEY=tu-clave-secreta-muy-larga-aqui-cambiar-esto
DEBUG=False
ALLOWED_HOSTS=tu-dominio.onrender.com
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret
```

**IMPORTANTE:**
- Obtén `CLOUDINARY_*` desde tu panel de Cloudinary
- Usa una `SECRET_KEY` fuerte (genera una con: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)
- La `DATABASE_URL` puedes obtenerla al crear una BD PostgreSQL en Render

### 4. **Configura la base de datos PostgreSQL en Render**
   - En Render, ve a "New" > "PostgreSQL"
   - Crea una base de datos
   - Copia la `DATABASE_URL` y pégala en las variables de entorno de tu web service

### 5. **Verifica que Render ejecute el build.sh**
   - En Render, la configuración debe detectar automáticamente `.render.yaml`
   - Si no, configura manualmente:
     - **Build Command**: `bash build.sh`
     - **Start Command**: `gunicorn djangocrud.wsgi:application --bind 0.0.0.0:$PORT`

### 6. **Haz push a GitHub**
```bash
git add .
git commit -m "Configurar para Render.com"
git push origin main
```

Render detectará automáticamente los cambios y hará deploy.

### 7. **Soluciona problemas comunes**

**Error: "SECRET_KEY environment variable is not set"**
- Añade `SECRET_KEY` en Environment Variables de Render

**Error: "OperationalError database does not exist"**
- Asegúrate que PostgreSQL esté creado en Render
- Añade correctamente `DATABASE_URL`

**Error: "DisallowedHost"**
- Actualiza `ALLOWED_HOSTS` con tu dominio de Render
- Formato: `tu-app.onrender.com`

**Los archivos de media no se cargan**
- Asegúrate que `CLOUDINARY_*` variables estén correctas
- Verifica que `cloudinary_storage` esté en `INSTALLED_APPS`

### 8. **Accede a tu aplicación**
Una vez desplegada, tu app estará disponible en:
```
https://tu-app-name.onrender.com
```

## Archivos que se añadieron para Render:
- `build.sh` - Script de build que instala dependencias y hace migraciones
- `.render.yaml` - Configuración de despliegue en Render
- `settings.py` - Actualizado con validaciones de variables de entorno

## Base de datos local vs Render:
- **Localmente**: Django usa `db.sqlite3`
- **En Render**: Django usa PostgreSQL (via `DATABASE_URL`)

¡Listo! Tu proyecto está preparado para Render.
