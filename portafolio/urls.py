from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('experiencia/', views.vista_experiencia, name='experiencia'),
    path('cursos/', views.vista_cursos, name='cursos'),
    path('reconocimientos/', views.vista_reconocimientos, name='reconocimientos'),
    path('productos/', views.vista_productos, name='productos'),
    path('garage/', views.vista_venta, name='venta'),
    path('exportar-pdf/', views.exportar_pdf, name='descargar_pdf'),
]