from django import template

register = template.Library()

@register.filter
def cloudinary_optimized(image, width=900):
    """
    Retorna uma URL otimizada do Cloudinary usando:
    f_auto = formato automático
    q_auto = qualidade automática
    w_X = largura desejada
    """
    if not image:
        return ""

    try:
        url = image.url
    except Exception:
        return ""

    if not url or "/upload/" not in url:
        return url

    transformation = f"f_auto,q_auto,w_{width}"

    # Evita duplicar transformação caso a URL já tenha sido transformada manualmente
    if transformation in url:
        return url

    return url.replace("/upload/", f"/upload/{transformation}/")
