from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import (
    DatosPersonales, ExperienciaLaboral, Reconocimientos, 
    CursosRealizados, ProductosAcademicos, ProductosLaborales, VentaGarage
)

def home(request):
    perfil = DatosPersonales.objects.first()
    # Traemos todo para que el recuadro del Modal pueda listar cada ítem
    todas_exp = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil)
    todos_cur = CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil)
    todos_rec = Reconocimientos.objects.filter(idperfilconqueestaactivo=perfil)
    todos_pro = ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil)
    todos_pro_lab = ProductosLaborales.objects.filter(idperfilconqueestaactivo=perfil)

    if perfil:
        if perfil.aptitudes:
            perfil.lista_aptitudes = [a.strip() for a in perfil.aptitudes.split(',')]
        if perfil.actitudes:
            perfil.lista_actitudes = [a.strip() for a in perfil.actitudes.split(',')]
            
    return render(request, 'home.html', {
        'perfil': perfil,
        'todas_exp': todas_exp,
        'todos_cur': todos_cur,
        'todos_rec': todos_rec,
        'todos_pro': todos_pro,
        'todos_pro_lab': todos_pro_lab
    })

def exportar_pdf(request):
    perfil = DatosPersonales.objects.first()
    tipo = request.GET.get('tipo', 'todo')
    
    if tipo == 'personalizado':
        ids_exp = request.GET.getlist('chk_exp')
        ids_cur = request.GET.getlist('chk_cur')
        ids_rec = request.GET.getlist('chk_rec')
        ids_pro = request.GET.getlist('chk_pro')
        ids_pro_lab = request.GET.getlist('chk_pro_lab')
        
        experiencias = ExperienciaLaboral.objects.filter(idexperiencilaboral__in=ids_exp)
        cursos = CursosRealizados.objects.filter(idcursorealizado__in=ids_cur)
        reconocimientos = Reconocimientos.objects.filter(idreconocimiento__in=ids_rec)
        academicos = ProductosAcademicos.objects.filter(idproductoacademico__in=ids_pro)
        # AQUÍ SE DEFINE LA VARIABLE QUE TE DABA ERROR:
        laborales = ProductosLaborales.objects.filter(idproductoslaborales__in=ids_pro_lab)
        titulo_doc = "Currículum Vitae Personalizado"
    else:
        experiencias = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil)
        cursos = CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil)
        reconocimientos = Reconocimientos.objects.filter(idperfilconqueestaactivo=perfil)
        academicos = ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil)
        # AQUÍ TAMBIÉN SE DEFINE PARA LA DESCARGA COMPLETA:
        laborales = ProductosLaborales.objects.filter(idperfilconqueestaactivo=perfil)
        titulo_doc = "Currículum Vitae"

    context = {
        'perfil': perfil,
        'experiencias': experiencias,
        'cursos': cursos,
        'reconocimientos': reconocimientos,
        'academicos': academicos,
        'laborales': laborales,
        'titulo_doc': titulo_doc,
        'user': request.user,
        'perfil_foto_url': request.build_absolute_uri(perfil.foto.url) if perfil and perfil.foto else None
    }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="CV_{perfil.apellidos}.pdf"'
    
    template = get_template('pdf_cv.html')
    html = template.render(context)
    pisa.CreatePDF(html, dest=response)
    
    return response

# Vistas de navegación (se mantienen igual)
def vista_experiencia(request):
    perfil = DatosPersonales.objects.first()
    items = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    return render(request, 'experiencia.html', {'perfil': perfil, 'items': items})

def vista_cursos(request):
    perfil = DatosPersonales.objects.first()
    items = CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    return render(request, 'cursos.html', {'perfil': perfil, 'items': items})

def vista_reconocimientos(request):
    perfil = DatosPersonales.objects.first()
    items = Reconocimientos.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    return render(request, 'reconocimientos.html', {'perfil': perfil, 'items': items})

def vista_productos(request):
    perfil = DatosPersonales.objects.first()
    academicos = ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil)
    laborales = ProductosLaborales.objects.filter(idperfilconqueestaactivo=perfil)
    return render(request, 'productos.html', {'perfil': perfil, 'academicos': academicos, 'laborales': laborales})

def vista_venta(request):
    perfil = DatosPersonales.objects.first()
    items = VentaGarage.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    return render(request, 'venta.html', {'perfil': perfil, 'items': items})