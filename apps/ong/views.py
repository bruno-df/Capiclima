from django.http import JsonResponse
from django.views.generic import ListView, TemplateView, View

from .models import (
    Atividade,
    ConteudoSobre,
    DestaqueInicio,
    MembroEquipe,
    Opportunity,
    SecaoApoie,
    SecaoHome,
    SecaoSobre,
)


class IndexView(TemplateView):
    """Pagina inicial do CapiClima — conteudo dinamico do banco de dados."""

    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Inicio"
        context["destaques"] = DestaqueInicio.objects.filter(
            ativo=True
        ).order_by("ordem", "id")
        context["atividades_destaque"] = Atividade.objects.filter(
            destaque=True, ativo=True
        )[:3]

        # Contadores em tempo real
        context["total_atividades"] = Atividade.objects.filter(ativo=True).count()
        context["total_colaboradores"] = MembroEquipe.objects.count()

        # Secao editavel da home (singleton)
        context["secao_home"] = SecaoHome.load()
        return context


class SobreView(TemplateView):
    """Pagina Sobre — secoes e equipe do banco de dados."""

    template_name = "pages/sobre.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sobre"
        context["secao_sobre"] = SecaoSobre.load()
        context["conteudos"] = ConteudoSobre.objects.all()
        context["equipe"] = MembroEquipe.objects.all()
        return context


class AtividadesView(ListView):
    """Pagina de Atividades — lista dinamica com paginacao."""

    template_name = "pages/atividades.html"
    model = Atividade
    context_object_name = "atividades"
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset().filter(ativo=True)
        ano = self.request.GET.get("ano")
        if ano:
            queryset = queryset.filter(data__year=ano)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Atividades"
        # Anos disponiveis para o filtro (apenas atividades ativas)
        context["anos"] = Atividade.objects.filter(ativo=True).dates(
            "data", "year", order="DESC"
        )
        context["ano_selecionado"] = self.request.GET.get("ano", "")
        return context


class OportunidadesView(TemplateView):
    """Pagina de Oportunidades — dados dinamicos do banco."""

    template_name = "pages/oportunidades.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Oportunidades"
        context["oportunidades"] = Opportunity.abertas().order_by(
            "ordem", "data_inicio"
        )
        return context


class ColaboradoresView(TemplateView):
    """Pagina Colaboradores — equipe e membros do CapiClima."""

    template_name = "pages/colaboradores.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Colaboradores"
        context["equipe"] = MembroEquipe.objects.all()
        return context


class ApoieView(TemplateView):
    """Pagina Como Apoiar — com dados dinamicos do SecaoApoie e SiteConfig."""

    template_name = "pages/apoie.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Apoie"
        context["secao_apoie"] = SecaoApoie.load()
        return context


class StatsAPIView(View):
    """Endpoint JSON para contadores em tempo real da home."""

    def get(self, request, *args, **kwargs):
        data = {
            "total_atividades": Atividade.objects.filter(ativo=True).count(),
            "total_colaboradores": MembroEquipe.objects.count(),
        }
        return JsonResponse(data)
