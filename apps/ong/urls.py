from django.urls import path
from . import views

app_name = 'ong'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('sobre/', views.SobreView.as_view(), name='sobre'),
    path('atividades/', views.AtividadesView.as_view(), name='atividades'),
    path('oportunidades/', views.OportunidadesView.as_view(), name='oportunidades'),
    path('apoie/', views.ApoieView.as_view(), name='apoie'),
]
