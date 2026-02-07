from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from xhtml2pdf import pisa
from .models import (
    DatosPersonales, ExperienciaLaboral, Reconocimientos, 
    CursosRealizados, ProductosAcademicos, ProductosLaborales, VentaGarage
)

def home(request):
    # Si el usuario está logueado, intentamos mostrar SU perfil
    if request.user.is_authenticated:
        perfil = DatosPersonales.objects.filter(usuario=request.user).first()
        # Si no tiene perfil, mostramos el primero público o vacío
        if not perfil:
            perfil = DatosPersonales.objects.first()
    else:
        perfil = DatosPersonales.objects.first()

    todas_exp = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil) if perfil else []
    todos_cur = CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil) if perfil else []
    todos_rec = Reconocimientos.objects.filter(idperfilconqueestaactivo=perfil) if perfil else []
    todos_pro = ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil) if perfil else []
    todos_pro_lab = ProductosLaborales.objects.filter(idperfilconqueestaactivo=perfil) if perfil else []

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
    # Intenta obtener el perfil del usuario logueado si existe
    if request.user.is_authenticated:
        perfil_usuario = DatosPersonales.objects.filter(usuario=request.user).first()
        if perfil_usuario:
            perfil = perfil_usuario

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
        if foto_url.startswith('http'):
            perfil_foto_url = foto_url
        else:
            perfil_foto_url = request.build_absolute_uri(foto_url)

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
    if perfil:
        response['Content-Disposition'] = f'attachment; filename="CV_{perfil.apellidos}.pdf"'
    else:
        response['Content-Disposition'] = f'attachment; filename="CV_Generico.pdf"'
    
    template = get_template('pdf_cv.html')
    html = template.render(context)
    pisa.CreatePDF(html, dest=response)
    
    return response

# Vistas de navegación (Mantienen la lógica original)
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

def error_404(request, exception):
    return render(request, '404.html', status=404)


# =======================================================
# NUEVAS FUNCIONES DE GESTIÓN (USUARIO Y ADMIN)
# =======================================================

# 1. Configuración del Perfil (Para el Usuario)
@login_required
def configuracion_perfil(request):
    # Busca el perfil del usuario logueado
    perfil = DatosPersonales.objects.filter(usuario=request.user).first()
    mensaje = None

    if request.method == 'POST':
        # Si no tiene perfil, se crea uno nuevo vinculado a este usuario
        if not perfil:
            perfil = DatosPersonales(usuario=request.user)
        
        # Guardamos los datos que vienen del formulario
        try:
            perfil.nombres = request.POST.get('nombres')
            perfil.apellidos = request.POST.get('apellidos')
            perfil.numerocedula = request.POST.get('numerocedula')
            perfil.nacionalidad = request.POST.get('nacionalidad')
            perfil.lugarnacimiento = request.POST.get('lugarnacimiento')
            perfil.fechanacimiento = request.POST.get('fechanacimiento')
            perfil.sexo = request.POST.get('sexo')
            perfil.estadocivil = request.POST.get('estadocivil')
            perfil.licenciaconducir = request.POST.get('licenciaconducir')
            perfil.direcciondomiciliaria = request.POST.get('direcciondomiciliaria')
            perfil.descripcionperfil = request.POST.get('descripcionperfil')
            
            if request.FILES.get('foto'):
                perfil.foto = request.FILES.get('foto')

            perfil.save()
            mensaje = "¡Perfil actualizado correctamente!"
        except Exception as e:
            mensaje = f"Error al guardar: {e}"

    return render(request, 'configuracion_perfil.html', {'perfil': perfil, 'mensaje': mensaje})


# 2. Panel Maestro (Para el Admin)
@user_passes_test(lambda u: u.is_staff)
def panel_master(request):
    # Lista todos los usuarios menos los superusuarios
    usuarios = User.objects.all().order_by('-date_joined')
    return render(request, 'panel_master.html', {'usuarios': usuarios})

# 3. Acción de Admin (Bloquear/Eliminar)
@user_passes_test(lambda u: u.is_staff)
def accion_usuario(request, user_id, accion):
    usuario_objetivo = get_object_or_404(User, id=user_id)
    
    # Evitar que el admin se elimine a sí mismo
    if usuario_objetivo == request.user:
        return redirect('panel_master')

    if accion == 'bloquear':
        usuario_objetivo.is_active = False
        usuario_objetivo.save()
    elif accion == 'activar':
        usuario_objetivo.is_active = True
        usuario_objetivo.save()
    elif accion == 'eliminar':
        usuario_objetivo.delete()
    
    return redirect('panel_master')