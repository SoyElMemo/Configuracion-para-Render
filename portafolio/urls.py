from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('experiencia/', views.vista_experiencia, name='experiencia'),
    path('cursos/', views.vista_cursos, name='cursos'),
    path('reconocimientos/', views.vista_reconocimientos, name='reconocimientos'),
    path('productos/', views.vista_productos, name='productos'),
    path('venta/', views.vista_venta, name='venta'),
    path('exportar-pdf/', views.exportar_pdf, name='descargar_pdf'),
    
    # --- RUTAS NUEVAS ---
    # 1. Donde el usuario edita su perfil
    path('configuracion/', views.configuracion_perfil, name='configuracion_perfil'),
    
    # 2. Donde el Admin ve a todos
    path('master-panel/', views.panel_master, name='panel_master'),
    
    # 3. Ruta lógica para bloquear/eliminar (no tiene vista propia, solo redirige)
    path('admin-accion/<int:user_id>/<str:accion>/', views.accion_usuario, name='accion_usuario'),
]