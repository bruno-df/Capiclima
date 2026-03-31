from django.shortcuts import render
from django.views.generic import TemplateView, ListView


class IndexView(TemplateView):
    """Página inicial do CapiClima"""
    template_name = 'pages/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Início'
        return context


class SobreView(TemplateView):
    """Página Sobre o CapiClima"""
    template_name = 'pages/sobre.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sobre'
        return context


class AtividadesView(TemplateView):
    """Página de Atividades"""
    template_name = 'pages/atividades.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Atividades'
        context['anos'] = [2025, 2024]  # Lista de anos com atividades
        return context


class OportunidadesView(TemplateView):
    """Página de Oportunidades de Voluntariado"""
    template_name = 'pages/oportunidades.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Oportunidades'
        return context


class ApoieView(TemplateView):
    """Página Como Apoiar"""
    template_name = 'pages/apoie.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Apoie'
        return context
