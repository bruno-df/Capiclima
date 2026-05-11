from .models import ConfiguracaoSite


def configuracao_site(request):
    """
    Context processor que disponibiliza a ConfiguracaoSite
    em TODOS os templates do projeto.

    Uso nos templates: {{ config_site.email }}, {{ config_site.instagram_url }}, etc.
    """
    try:
        config = ConfiguracaoSite.load()
    except Exception:
        config = None
    return {'config_site': config}
