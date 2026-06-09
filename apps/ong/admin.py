from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Atividade,
    ConteudoSobre,
    DestaqueInicio,
    MembroEquipe,
    Opportunity,
    SiteConfig,
    SiteSection,
)
from .permissions import user_has_cms_access


admin.site.site_header = "CapiClima - Painel de Gestao"
admin.site.site_title = "CapiClima CMS"
admin.site.index_title = "Gerenciar conteudo do site"
admin.site.has_permission = lambda request: user_has_cms_access(request.user)


class ImagePreviewMixin:
    readonly_fields = ("imagem_preview",)

    @admin.display(description="Preview")
    def imagem_preview(self, obj):
        image = self._get_preview_image(obj)
        if not image:
            return "Sem imagem"
        try:
            url = image.url
        except (AttributeError, ValueError):
            return "Sem imagem"
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">'
            '<img src="{}" style="max-width:180px;max-height:120px;object-fit:cover;border-radius:6px;" />'
            "</a>",
            url,
            url,
        )

    def _get_preview_image(self, obj):
        for field_name in ("imagem", "foto", "logo", "qrcode_pix", "favicon"):
            image = getattr(obj, field_name, None)
            if image:
                return image
        return None


@admin.register(SiteSection)
class SiteSectionAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("nome", "slug", "titulo", "ativo", "ordem", "atualizado_em")
    list_editable = ("ativo", "ordem")
    list_filter = ("ativo",)
    search_fields = ("nome", "slug", "titulo", "texto_principal")
    prepopulated_fields = {"slug": ("nome",)}
    fieldsets = (
        ("Identificacao", {"fields": ("nome", "slug", "ativo", "ordem")}),
        ("Conteudo", {"fields": ("titulo", "texto_principal", "imagem", "imagem_preview")}),
        ("Chamada", {"fields": ("botao_texto", "botao_url"), "classes": ("collapse",)}),
    )


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ("titulo", "data_inicio", "data_fim", "ativo", "ordem", "esta_aberta")
    list_editable = ("ativo", "ordem")
    list_filter = ("ativo", "data_inicio", "data_fim")
    search_fields = ("titulo", "descricao", "link")
    date_hierarchy = "data_inicio"
    fieldsets = (
        ("Oportunidade", {"fields": ("titulo", "descricao", "link")}),
        ("Datas e exibicao", {"fields": ("data_inicio", "data_fim", "ativo", "ordem")}),
    )


@admin.register(DestaqueInicio)
class DestaqueInicioAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("titulo", "subtitulo", "ativo", "ordem")
    list_editable = ("ativo", "ordem")
    list_filter = ("ativo",)
    search_fields = ("titulo", "subtitulo")
    fieldsets = (
        ("Conteudo do banner", {"fields": ("titulo", "subtitulo", "imagem", "imagem_preview")}),
        ("Exibicao", {"fields": ("ativo", "ordem")}),
    )


@admin.register(ConteudoSobre)
class ConteudoSobreAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("titulo_secao", "icone", "ordem")
    list_editable = ("ordem",)
    search_fields = ("titulo_secao", "texto_informativo")
    fieldsets = (
        ("Conteudo", {"fields": ("titulo_secao", "texto_informativo", "imagem", "imagem_preview")}),
        (
            "Aparencia",
            {
                "fields": ("icone", "ordem"),
                "description": "Use icones do Font Awesome. Ex: fas fa-leaf",
            },
        ),
    )


@admin.register(Atividade)
class AtividadeAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("nome", "tipo", "data", "local", "ativo", "destaque")
    list_editable = ("ativo", "destaque")
    list_filter = ("ativo", "destaque", "tipo", "data")
    search_fields = ("nome", "descricao", "local", "tipo")
    date_hierarchy = "data"
    fieldsets = (
        (
            "Informacoes da atividade",
            {"fields": ("nome", "tipo", "data", "horario", "local", "descricao")},
        ),
        ("Imagem", {"fields": ("imagem", "imagem_local", "imagem_preview")}),
        ("Exibicao", {"fields": ("ativo", "destaque")}),
    )


@admin.register(MembroEquipe)
class MembroEquipeAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("nome", "cargo", "ordem")
    list_editable = ("ordem",)
    search_fields = ("nome", "cargo", "bio")
    fieldsets = (
        ("Dados pessoais", {"fields": ("nome", "cargo", "foto", "foto_local", "imagem_preview", "bio")}),
        ("Links", {"fields": ("instagram", "linkedin"), "classes": ("collapse",)}),
        ("Exibicao", {"fields": ("ordem",)}),
    )


@admin.register(SiteConfig)
class SiteConfigAdmin(ImagePreviewMixin, admin.ModelAdmin):
    readonly_fields = ("imagem_preview", "logo_preview", "qrcode_preview")
    fieldsets = (
        ("Identidade do site", {"fields": ("nome_site", "slogan", "logo", "logo_preview", "favicon")}),
        ("Contato", {"fields": ("email", "telefone", "whatsapp", "endereco")}),
        ("Redes sociais", {"fields": ("instagram_url", "twitter_url", "facebook_url", "youtube_url")}),
        ("Doacoes", {"fields": ("chave_pix", "qrcode_pix", "qrcode_preview")}),
        ("Rodape", {"fields": ("texto_rodape",)}),
    )

    @admin.display(description="Logo atual")
    def logo_preview(self, obj):
        return self._render_field_preview(obj, "logo")

    @admin.display(description="QR Code atual")
    def qrcode_preview(self, obj):
        return self._render_field_preview(obj, "qrcode_pix")

    def _render_field_preview(self, obj, field_name):
        image = getattr(obj, field_name, None)
        if not image:
            return "Sem imagem"
        try:
            url = image.url
        except (AttributeError, ValueError):
            return "Sem imagem"
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">'
            '<img src="{}" style="max-width:180px;max-height:120px;object-fit:contain;border-radius:6px;" />'
            "</a>",
            url,
            url,
        )

    def has_add_permission(self, request):
        return not SiteConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
