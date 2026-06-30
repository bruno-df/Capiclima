from django.http import JsonResponse
from django.views.generic import ListView, TemplateView, View

from .models import (
    Atividade,
    DestaqueInicio,
    MembroEquipe,
    Opportunity,
    Parceiro,
    SecaoApoie,
    SecaoHome,
    SiteConfig,
)


class IndexView(TemplateView):
    """Pagina inicial do CapiClima — conteudo dinamico do banco de dados."""

    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Inicio"
        context["secao_home"] = SecaoHome.load()
        context["destaques"] = DestaqueInicio.objects.filter(
            ativo=True
        ).order_by("ordem", "id")
        context["atividades_destaque"] = Atividade.objects.filter(
            destaque=True, ativo=True
        )[:3]

        # Contadores em tempo real
        context["total_atividades"] = Atividade.objects.filter(ativo=True).count()
        context["total_equipe"] = MembroEquipe.objects.count()

        context["parceiros"] = Parceiro.objects.filter(
            ativo=True
        ).order_by("ordem", "nome")
        return context


class SobreView(TemplateView):
    """Pagina Sobre — secoes e equipe do banco de dados."""

    template_name = "pages/sobre.html"

    def get_context_data(self, **kwargs):
        from .models import ConteudoSobre, SecaoSobre

        context = super().get_context_data(**kwargs)
        context["title"] = "Sobre"
        context["secao_sobre"] = SecaoSobre.load()
        context["conteudos"] = ConteudoSobre.objects.all()
        context["equipe"] = MembroEquipe.objects.all()

        # Contadores em tempo real
        context["total_atividades"] = Atividade.objects.filter(ativo=True).count()
        context["total_colaboradores"] = MembroEquipe.objects.count()

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


class EquipeView(TemplateView):
    """Pagina Equipe — equipe e membros do CapiClima."""

    template_name = "pages/equipe.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Equipe"
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
            "total_equipe": MembroEquipe.objects.count(),
        }
        return JsonResponse(data)


def health_check(request):
    """
    Keep-alive endpoint para o Render e o Supabase.

    Chamado periodicamente pelo UptimeRobot (a cada 14 min) para:
    - Render: evitar a suspensão por inatividade (limite: 15 min).
    - Supabase: evitar a pausa do projeto por inatividade (limite: 7 dias).

    A query via SiteConfig.load() é a mesma usada pelas views públicas do
    projeto — padrão SingletonMixin — e garante uma round-trip real ao banco
    sem exigir autenticação nem dependências extras.
    """
    SiteConfig.load()
    return JsonResponse({"status": "ok"})
