from .models import ExperienciaLaboral, CursosRealizados, ProductosAcademicos, Reconocimientos, ProductosLaborales

def pdf_data(request):
    return {
        'todas_exp': ExperienciaLaboral.objects.filter(activarparaqueseveaenfront=True),
        'todos_cur': CursosRealizados.objects.filter(activarparaqueseveaenfront=True),
        'todos_pro': ProductosAcademicos.objects.filter(activarparaqueseveaenfront=True),
        'todos_rec': Reconocimientos.objects.filter(activarparaqueseveaenfront=True),
        'todos_pro_lab': ProductosLaborales.objects.filter(activarparaqueseveaenfront=True),
    }