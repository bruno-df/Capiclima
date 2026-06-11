from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    Atividade,
    ConteudoSobre,
    DestaqueInicio,
    MembroEquipe,
    Opportunity,
    SecaoApoie,
    SecaoHome,
    SecaoSobre,
    SiteConfig,
)
from .permissions import user_has_cms_access


# ---------------------------------------------------------------------------
# PROBLEMA 3 — UX geral do admin
# ---------------------------------------------------------------------------
admin.site.site_header = "Capiclima \u2014 Painel de Gest\u00e3o"
admin.site.site_title = "Capiclima CMS"
admin.site.index_title = "Bem-vindo ao painel"
admin.site.has_permission = lambda request: user_has_cms_access(request.user)


# ---------------------------------------------------------------------------
# Mixins reutilizaveis
# ---------------------------------------------------------------------------
class ImagePreviewMixin:
    """Mixin que adiciona preview de imagem em qualquer admin com campo de imagem."""

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
        for field_name in ("imagem", "imagem_banner", "foto", "logo", "qrcode_pix", "favicon"):
            image = getattr(obj, field_name, None)
            if image:
                return image
        return None


class SingletonAdminMixin:
    """Mixin para admins de modelos singleton — redireciona lista para formulario."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = self.model.load()
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return redirect(
            reverse(f"admin:{app_label}_{model_name}_change", args=[obj.pk])
        )


# ---------------------------------------------------------------------------
# PROBLEMA 2 — Admin agrupado por secao
# ---------------------------------------------------------------------------

# ===== INICIO =====

@admin.register(SecaoHome)
class SecaoHomeAdmin(SingletonAdminMixin, ImagePreviewMixin, admin.ModelAdmin):
    readonly_fields = ("imagem_preview", "banner_preview", "parceiros_preview")
    fieldsets = (
        ("Banner Principal (Hero)", {
            "fields": ("titulo_principal", "subtitulo", "imagem_banner", "banner_preview"),
            "description": "Conteudo exibido no topo da pagina inicial.",
        }),
        ("Juventudes em Acao", {
            "fields": ("titulo_juventudes", "texto_juventudes", "imagem_juventudes", "imagem_preview"),
        }),
        ("Parceiros", {
            "fields": ("titulo_parceiros", "texto_parceiros", "imagem_parceiros", "parceiros_preview"),
        }),
        ("Chamada para Acao (CTA)", {
            "fields": ("titulo_cta", "texto_cta", "link_cta"),
            "description": "Bloco de chamada no final da pagina inicial.",
        }),
    )

    @admin.display(description="Preview do Banner")
    def banner_preview(self, obj):
        if not obj.imagem_banner:
            return "Sem imagem"
        try:
            url = obj.imagem_banner.url
        except (AttributeError, ValueError):
            return "Sem imagem"
        return format_html(
            '<img src="{}" style="max-width:300px;max-height:150px;object-fit:cover;border-radius:6px;" />',
            url,
        )

    @admin.display(description="Preview dos Parceiros")
    def parceiros_preview(self, obj):
        if not obj.imagem_parceiros:
            return "Sem imagem"
        try:
            url = obj.imagem_parceiros.url
        except (AttributeError, ValueError):
            return "Sem imagem"
        return format_html(
            '<img src="{}" style="max-width:300px;max-height:150px;object-fit:contain;border-radius:6px;" />',
            url,
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


@admin.register(DestaqueInicio)
class DestaqueInicioAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("titulo", "ativo", "ordem", "link_botao")
    list_editable = ("ativo", "ordem")
    list_filter = ("ativo",)
    search_fields = ("titulo", "subtitulo", "link_botao")
    fieldsets = (
        (
            "Conteúdo do banner",
            {
                "fields": (
                    "titulo",
                    "subtitulo",
                    "imagem",
                    "imagem_preview",
                )
            },
        ),
        (
            "Botão do banner",
            {
                "fields": (
                    "texto_botao",
                    "link_botao",
                    "abrir_nova_aba",
                ),
                "description": "Se o link ficar vazio, o botão não aparece no banner.",
            },
        ),
        (
            "Exibição",
            {
                "fields": (
                    "ativo",
                    "ordem",
                )
            },
        ),
    )


# ===== APOIE =====

@admin.register(SecaoApoie)
class SecaoApoieAdmin(SingletonAdminMixin, admin.ModelAdmin):
    fieldsets = (
        ("Voluntariado", {
            "fields": ("texto_voluntariado", "link_voluntariado"),
            "description": "Secao de voluntariado na pagina Apoie.",
        }),
        ("Doacao Financeira", {
            "fields": ("texto_doacao", "link_doacao"),
        }),
        ("Parcerias Empresariais", {
            "fields": ("texto_parcerias", "link_parcerias"),
        }),
        ("Compartilhe", {
            "fields": ("texto_compartilhe",),
        }),
    )


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "tipo",
        "data_fim",
        "ativo",
        "ordem",
        "esta_aberta",
    )

    list_editable = (
        "tipo",
        "data_fim",
        "ativo",
        "ordem",
    )

    list_filter = (
        "ativo",
        "tipo",
        "data_fim",
    )

    search_fields = (
        "titulo",
        "tipo",
        "descricao",
        "link",
    )

    date_hierarchy = "data_fim"

    fieldsets = (
        (
            "Dados da oportunidade",
            {
                "fields": (
                    "titulo",
                    "tipo",
                    "descricao",
                )
            },
        ),
        (
            "Inscrição",
            {
                "fields": (
                    "link",
                    "data_inicio",
                    "data_fim",
                ),
                "description": "Se o link ficar vazio, o botão de inscrição não será exibido no site.",
            },
        ),
        (
            "Exibição no site",
            {
                "fields": (
                    "ativo",
                    "ordem",
                )
            },
        ),
    )


# ===== SOBRE =====

@admin.register(SecaoSobre)
class SecaoSobreAdmin(SingletonAdminMixin, ImagePreviewMixin, admin.ModelAdmin):
    readonly_fields = ("imagem_preview",)
    fieldsets = (
        ("Conteudo Principal", {
            "fields": ("titulo", "texto_principal", "imagem", "imagem_preview"),
            "description": "Texto institucional exibido na pagina Sobre.",
        }),
        ("Missao, Visao e Valores", {
            "fields": ("missao", "visao", "valores"),
            "classes": ("collapse",),
            "description": "Campos opcionais. Se preenchidos, aparecem como secoes separadas.",
        }),
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


# ===== CONFIGURACOES GLOBAIS =====

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
class SiteConfigAdmin(SingletonAdminMixin, ImagePreviewMixin, admin.ModelAdmin):
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


