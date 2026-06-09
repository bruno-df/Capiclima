from django.views.generic import ListView, TemplateView

from .models import (
    Atividade,
    ConteudoSobre,
    DestaqueInicio,
    MembroEquipe,
    Opportunity,
    SiteSection,
)


class IndexView(TemplateView):
    """Pagina inicial do CapiClima — conteudo dinamico do banco de dados."""

    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Inicio"
        context["destaques"] = DestaqueInicio.objects.filter(ativo=True)
        context["atividades_destaque"] = Atividade.objects.filter(
            destaque=True, ativo=True
        )[:3]

        # Secoes editaveis da home
        _sections = SiteSection.objects.filter(ativo=True)
        context["secao_juventudes"] = _sections.filter(slug="home-juventudes").first()
        context["secao_parceiros"] = _sections.filter(slug="home-parceiros").first()
        context["secao_cta"] = _sections.filter(slug="home-cta").first()
        return context


class SobreView(TemplateView):
    """Pagina Sobre — secoes e equipe do banco de dados."""

    template_name = "pages/sobre.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sobre"
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
    """Pagina Como Apoiar — com dados dinamicos do SiteConfig."""

    template_name = "pages/apoie.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Apoie"
        # Secoes editaveis da pagina Apoie
        _sections = SiteSection.objects.filter(ativo=True)
        context["secao_voluntariado"] = _sections.filter(
            slug="apoie-voluntariado"
        ).first()
        context["secao_doacao"] = _sections.filter(slug="apoie-doacao").first()
        context["secao_parcerias"] = _sections.filter(slug="apoie-parcerias").first()
        context["secao_compartilhe"] = _sections.filter(
            slug="apoie-compartilhe"
        ).first()
        return context
