from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import DestaqueInicio, ConteudoSobre, Atividade, MembroEquipe


class IndexView(TemplateView):
    """Página inicial do CapiClima — conteúdo dinâmico do banco de dados."""
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Início'
        context['destaques'] = DestaqueInicio.objects.filter(ativo=True)
        context['atividades_destaque'] = Atividade.objects.filter(destaque=True)[:3]
        return context


class SobreView(TemplateView):
    """Página Sobre — seções e equipe do banco de dados."""
    template_name = 'pages/sobre.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sobre'
        context['conteudos'] = ConteudoSobre.objects.all()
        context['equipe'] = MembroEquipe.objects.all()
        return context


class AtividadesView(ListView):
    """Página de Atividades — lista dinâmica com paginação."""
    template_name = 'pages/atividades.html'
    model = Atividade
    context_object_name = 'atividades'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        ano = self.request.GET.get('ano')
        if ano:
            queryset = queryset.filter(data__year=ano)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Atividades'
        # Anos disponíveis para o filtro
        context['anos'] = (
            Atividade.objects.dates('data', 'year', order='DESC')
        )
        context['ano_selecionado'] = self.request.GET.get('ano', '')
        return context


class OportunidadesView(TemplateView):
    """Página de Oportunidades de Voluntariado."""
    template_name = 'pages/oportunidades.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Oportunidades'
        return context


class ColaboradoresView(TemplateView):
    """Página Colaboradores — equipe e membros do CapiClima."""
    template_name = 'pages/colaboradores.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Colaboradores'
        context['equipe'] = MembroEquipe.objects.all()
        return context


class ApoieView(TemplateView):
    """Página Como Apoiar — com dados dinâmicos do ConfiguracaoSite."""
    template_name = 'pages/apoie.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Apoie'
        return context
