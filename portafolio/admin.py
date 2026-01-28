from django.contrib import admin
from django.utils.html import format_html
from .models import (
    DatosPersonales, ExperienciaLaboral, Reconocimientos, 
    CursosRealizados, ProductosAcademicos, ProductosLaborales, VentaGarage
)

# --- CONFIGURACIÓN ESTÉTICA DEL PANEL ---
admin.site.site_header = "Panel Administrativo - Guillermo"
admin.site.index_title = "Gestión de Portafolio Profesional"
admin.site.site_title = "Guillermo Admin"

@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'numerocedula', 'perfilactivo', 'ver_foto')
    search_fields = ('nombres', 'apellidos', 'numerocedula')
    
    def ver_foto(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="width: 40px; height: 40px; border-radius: 50%;" />', obj.foto.url)
        return "Sin foto"
    ver_foto.short_description = 'Foto'

@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = ('cargodesempenado', 'nombrempresa', 'fechainiciogestion', 'activarparaqueseveaenfront')
    list_filter = ('activarparaqueseveaenfront', 'nombrempresa')
    list_editable = ('activarparaqueseveaenfront',)
    search_fields = ('cargodesempenado', 'nombrempresa', 'descripcionfunciones')

@admin.register(CursosRealizados)
class CursosRealizadosAdmin(admin.ModelAdmin):
    list_display = ('nombrecurso', 'entidadpatrocinadora', 'totalhoras', 'activarparaqueseveaenfront')
    list_filter = ('activarparaqueseveaenfront', 'entidadpatrocinadora')
    list_editable = ('activarparaqueseveaenfront',)
    search_fields = ('nombrecurso', 'entidadpatrocinadora')

@admin.register(Reconocimientos)
class ReconocimientosAdmin(admin.ModelAdmin):
    list_display = ('tiporeconocimiento', 'entidadpatrocinadora', 'fechareconocimiento', 'activarparaqueseveaenfront')
    list_filter = ('activarparaqueseveaenfront', 'tiporeconocimiento')
    list_editable = ('activarparaqueseveaenfront',)
    search_fields = ('tiporeconocimiento', 'descripcionreconocimiento', 'entidadpatrocinadora')

@admin.register(ProductosAcademicos)
class ProductosAcademicosAdmin(admin.ModelAdmin):
    list_display = ('nombrerecurso', 'clasificador', 'activarparaqueseveaenfront')
    list_filter = ('activarparaqueseveaenfront', 'clasificador')
    list_editable = ('activarparaqueseveaenfront',)
    search_fields = ('nombrerecurso', 'clasificador', 'descripcion')

@admin.register(ProductosLaborales)
class ProductosLaboralesAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'fechaproducto', 'activarparaqueseveaenfront')
    list_filter = ('activarparaqueseveaenfront',)
    list_editable = ('activarparaqueseveaenfront',)
    search_fields = ('nombreproducto', 'descripcion')

@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    # Usamos 'valordelbien' y 'foto' que son tus nombres reales en models.py
    list_display = ('nombreproducto', 'valordelbien', 'estadoproducto', 'activarparaqueseveaenfront', 'ver_foto')
    list_filter = ('activarparaqueseveaenfront', 'estadoproducto')
    list_editable = ('valordelbien', 'activarparaqueseveaenfront')
    search_fields = ('nombreproducto', 'descripcion')

    def ver_foto(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 5px;" />', obj.foto.url)
        return "Sin imagen"
    ver_foto.short_description = 'Imagen'