from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required, user_passes_test
from xhtml2pdf import pisa
from .models import (
    DatosPersonales, ExperienciaLaboral, Reconocimientos, 
    CursosRealizados, ProductosAcademicos, ProductosLaborales, VentaGarage
)

# VISTA HOME
def home(request):
    perfil = DatosPersonales.objects.first()
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

# EXPORTAR PDF
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
        laborales = ProductosLaborales.objects.filter(idproductoslaborales__in=ids_pro_lab)
        titulo_doc = "Currículum Vitae Personalizado"
    else:
        experiencias = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil)
        cursos = CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil)
        reconocimientos = Reconocimientos.objects.filter(idperfilconqueestaactivo=perfil)
        academicos = ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil)
        laborales = ProductosLaborales.objects.filter(idperfilconqueestaactivo=perfil)
        titulo_doc = "Currículum Vitae"

    perfil_foto_url = None
    if perfil and perfil.foto:
        foto_url = perfil.foto.url
        perfil_foto_url = foto_url if foto_url.startswith('http') else request.build_absolute_uri(foto_url)

    context = {
        'perfil': perfil,
        'experiencias': experiencias,
        'cursos': cursos,
        'reconocimientos': reconocimientos,
        'academicos': academicos,
        'laborales': laborales,
        'titulo_doc': titulo_doc,
        'user': request.user,
        'perfil_foto_url': perfil_foto_url
    }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="CV_{perfil.apellidos}.pdf"'
    template = get_template('pdf_cv.html')
    html = template.render(context)
    pisa.CreatePDF(html, dest=response)
    return response

# VISTAS DE NAVEGACIÓN
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

# --- NUEVAS FUNCIONES PARA SEPARACIÓN USUARIO/ADMIN ---

@login_required
def dashboard_usuario(request):
    # Trae el perfil del usuario logueado
    perfil = DatosPersonales.objects.filter(usuario=request.user).first()
    return render(request, 'dashboard_usuario.html', {'perfil': perfil})

@user_passes_test(lambda u: u.is_staff)
def dashboard_admin(request):
    # El admin ve todos los perfiles registrados
    perfiles = DatosPersonales.objects.all()
    return render(request, 'dashboard_admin.html', {'perfiles': perfiles})

def error_404(request, exception):
    return render(request, '404.html', status=404)