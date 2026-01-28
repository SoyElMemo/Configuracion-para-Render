from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from django_countries.fields import CountryField

# --- VALIDACIONES ---
def validar_fecha_nacimiento(value):
    today = date.today()
    if value >= today:
        raise ValidationError('La fecha de nacimiento no puede ser hoy ni futura.')
    if value.year > (today.year - 14):
        raise ValidationError('Debes tener al menos 14 años para registrar un perfil.')

# --- 1. DATOS PERSONALES ---
class DatosPersonales(models.Model):
    idperfil = models.AutoField(primary_key=True)
    foto = models.ImageField(upload_to='perfil/', null=True, blank=True)
    descripcionperfil = models.TextField(max_length=500, null=True, blank=True)
    perfilactivo = models.IntegerField(default=1)
    
    apellidos = models.CharField(max_length=60)
    nombres = models.CharField(max_length=60)
    nacionalidad = CountryField(blank_label='(Seleccionar país)', default='EC')
    lugarnacimiento = models.CharField(max_length=100)
    fechanacimiento = models.DateField(validators=[validar_fecha_nacimiento])
    numerocedula = models.CharField(max_length=10, unique=True)
    
    sexo = models.CharField(max_length=1, choices=[('H', 'Hombre'), ('M', 'Mujer')])
    estadocivil = models.CharField(max_length=50, choices=[('Soltero/a', 'Soltero/a'), ('Casado/a', 'Casado/a'), ('Divorciado/a', 'Divorciado/a'), ('Viudo/a', 'Viudo/a'), ('Unión Libre', 'Unión Libre')])
    licenciaconducir = models.CharField(max_length=20, choices=[('No', 'No posee'), ('Tipo A', 'Tipo A'), ('Tipo B', 'Tipo B'), ('Tipo C', 'Tipo C'), ('Tipo D', 'Tipo D'), ('Tipo E', 'Tipo E')])
    
    telefonoconvencional = models.CharField(max_length=15, null=True, blank=True)
    telefonofijo = models.CharField(max_length=15, null=True, blank=True)
    direcciontrabajo = models.CharField(max_length=100, null=True, blank=True)
    direcciondomiciliaria = models.CharField(max_length=100)
    sitioweb = models.URLField(max_length=200, null=True, blank=True)

    aptitudes = models.TextField(null=True, blank=True)
    actitudes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

# --- 2. EXPERIENCIA LABORAL ---
class ExperienciaLaboral(models.Model):
    idexperiencilaboral = models.AutoField(primary_key=True)
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    
    nombrempresa = models.CharField(max_length=100)
    lugarempresa = models.CharField(max_length=100)
    cargodesempenado = models.CharField(max_length=100)
    
    emailempresa = models.EmailField(max_length=100, null=True, blank=True)
    sitiowebempresa = models.URLField(max_length=100, null=True, blank=True)
    nombrecontactoempresarial = models.CharField(max_length=100, null=True, blank=True)
    telefonocontactoempresarial = models.CharField(max_length=20, null=True, blank=True)
    
    fechainiciogestion = models.DateField()
    fechafingestion = models.DateField(null=True, blank=True)
    
    descripcionfunciones = models.TextField(null=True, blank=True)
    rutacertificado = models.FileField(upload_to='certificados_laborales/', null=True, blank=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)

    @property
    def periodo_gestion(self):
        inicio = self.fechainiciogestion.strftime('%d/%m/%Y') if self.fechainiciogestion else "N/A"
        if self.fechafingestion:
            return f"{inicio} - {self.fechafingestion.strftime('%d/%m/%Y')}"
        return f"{inicio} - Actualidad"

    def clean(self):
        super().clean()
        # VALIDACIÓN RAZONABLE: No puede trabajar antes de nacer + 14 años
        nacimiento = self.idperfilconqueestaactivo.fechanacimiento
        if self.fechainiciogestion and nacimiento and self.fechainiciogestion.year < (nacimiento.year + 14):
            raise ValidationError(f'Incoherencia: Según la fecha de nacimiento ({nacimiento.year}), el usuario no podía trabajar en {self.fechainiciogestion.year}.')

        if self.fechainiciogestion and self.fechafingestion and self.fechafingestion < self.fechainiciogestion:
            raise ValidationError({'fechafingestion': 'La fecha de fin no puede ser anterior al inicio.'})

# --- 3. RECONOCIMIENTOS ---
class Reconocimientos(models.Model):
    idreconocimiento = models.AutoField(primary_key=True)
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    tiporeconocimiento = models.CharField(max_length=100)
    fechareconocimiento = models.DateField()
    descripcionreconocimiento = models.CharField(max_length=200)
    entidadpatrocinadora = models.CharField(max_length=100, null=True, blank=True)
    nombrecontactoauspicia = models.CharField(max_length=100, null=True, blank=True)
    telefonocontactoauspicia = models.CharField(max_length=20, null=True, blank=True)
    rutacertificado = models.FileField(upload_to='certificados_reconocimientos/', null=True, blank=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)

# --- 4. CURSOS REALIZADOS ---
class CursosRealizados(models.Model):
    idcursorealizado = models.AutoField(primary_key=True)
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombrecurso = models.CharField(max_length=150)
    totalhoras = models.IntegerField()
    fechainicio = models.DateField(null=True, blank=True)
    fechafin = models.DateField(null=True, blank=True)
    descripcioncurso = models.TextField(null=True, blank=True)
    entidadpatrocinadora = models.CharField(max_length=100, null=True, blank=True)
    nombrecontactoauspicia = models.CharField(max_length=100, null=True, blank=True)
    telefonocontactoauspicia = models.CharField(max_length=20, null=True, blank=True)
    emailempresapatrocinadora = models.EmailField(null=True, blank=True)
    rutacertificado = models.FileField(upload_to='certificados_cursos/', null=True, blank=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)

    def clean(self):
        if self.fechainicio and self.fechafin and self.fechafin < self.fechainicio:
            raise ValidationError({'fechafin': 'La fecha de fin del curso no puede ser anterior al inicio.'})

# --- 5. PRODUCTOS ACADEMICOS ---
class ProductosAcademicos(models.Model):
    idproductoacademico = models.AutoField(primary_key=True)
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombrerecurso = models.CharField(max_length=150)
    clasificador = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)

# --- 6. PRODUCTOS LABORALES ---
class ProductosLaborales(models.Model):
    idproductoslaborales = models.AutoField(primary_key=True)
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombreproducto = models.CharField(max_length=150)
    fechaproducto = models.DateField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)

# --- 7. VENTA GARAGE ---
class VentaGarage(models.Model):
    idventagarage = models.AutoField(primary_key=True)
    idperfilconqueestaactivo = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE)
    nombreproducto = models.CharField(max_length=100)
    valordelbien = models.DecimalField(max_digits=10, decimal_places=2)
    foto = models.ImageField(upload_to='garage/', null=True, blank=True)
    estadoproducto = models.CharField(max_length=20, choices=[('Bueno', 'Bueno'), ('Regular', 'Regular')], default='Bueno')
    descripcion = models.TextField(null=True, blank=True)
    activarparaqueseveaenfront = models.BooleanField(default=True)
    whatsapp = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.nombreproducto