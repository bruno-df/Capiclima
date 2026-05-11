from django.contrib import admin
from .models import DestaqueInicio, ConteudoSobre, Atividade, MembroEquipe, ConfiguracaoSite


# ============================================
# Branding do Admin
# ============================================
admin.site.site_header = "CapiClima — Painel de Gestão"
admin.site.site_title = "CapiClima Admin"
admin.site.index_title = "Gerenciar Conteúdo do Site"


# ============================================
# Admin: Destaques da Página Inicial
# ============================================
@admin.register(DestaqueInicio)
class DestaqueInicioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'subtitulo', 'ativo', 'ordem')
    list_editable = ('ativo', 'ordem')
    list_filter = ('ativo',)
    search_fields = ('titulo', 'subtitulo')


# ============================================
# Admin: Conteúdos da Página Sobre
# ============================================
@admin.register(ConteudoSobre)
class ConteudoSobreAdmin(admin.ModelAdmin):
    list_display = ('titulo_secao', 'icone', 'ordem')
    list_editable = ('ordem',)
    search_fields = ('titulo_secao',)
    fieldsets = (
        ('Conteúdo', {
            'fields': ('titulo_secao', 'texto_informativo', 'imagem')
        }),
        ('Aparência', {
            'fields': ('icone', 'ordem'),
            'description': 'Use ícones do Font Awesome. Ex: fas fa-leaf'
        }),
    )


# ============================================
# Admin: Atividades
# ============================================
@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data', 'local', 'destaque')
    list_editable = ('destaque',)
    list_filter = ('data', 'destaque')
    search_fields = ('nome', 'descricao', 'local')
    date_hierarchy = 'data'
    fieldsets = (
        ('Informações da Atividade', {
            'fields': ('nome', 'data', 'local', 'descricao', 'imagem')
        }),
        ('Exibição', {
            'fields': ('destaque',),
            'description': 'Marque "Destaque" para exibir esta atividade na página inicial.'
        }),
    )


# ============================================
# Admin: Membros da Equipe
# ============================================
@admin.register(MembroEquipe)
class MembroEquipeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cargo', 'ordem')
    list_editable = ('ordem',)
    search_fields = ('nome', 'cargo')
    fieldsets = (
        ('Dados Pessoais', {
            'fields': ('nome', 'cargo', 'foto', 'bio')
        }),
        ('Links', {
            'fields': ('linkedin',),
            'classes': ('collapse',),
        }),
        ('Exibição', {
            'fields': ('ordem',)
        }),
    )


# ============================================
# Admin: Configuração do Site (Singleton)
# ============================================
@admin.register(ConfiguracaoSite)
class ConfiguracaoSiteAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identidade do Site', {
            'fields': ('nome_site', 'slogan', 'logo', 'favicon')
        }),
        ('Contato', {
            'fields': ('email', 'telefone', 'whatsapp', 'endereco')
        }),
        ('Redes Sociais', {
            'fields': ('instagram_url', 'twitter_url', 'facebook_url', 'youtube_url')
        }),
        ('Doações', {
            'fields': ('chave_pix', 'qrcode_pix'),
            'description': 'Informações de Pix exibidas na página "Apoie".'
        }),
        ('Rodapé', {
            'fields': ('texto_rodape',)
        }),
    )

    def has_add_permission(self, request):
        """Impede criação de mais de 1 configuração."""
        return not ConfiguracaoSite.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Impede exclusão da configuração."""
        return False