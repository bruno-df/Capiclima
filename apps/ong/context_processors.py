from .models import SiteConfig


# Backwards-compatible alias kept for existing references.
ConfiguracaoSite = SiteConfig


def configuracao_site(request):
    """
    Context processor que disponibiliza a SiteConfig (singleton)
    em TODOS os templates do projeto.

    Uso nos templates: {{ config_site.email }}, {{ config_site.instagram_url }}, etc.
    """
    try:
        config = SiteConfig.load()
    except Exception:
        config = None
    return {"config_site": config}
