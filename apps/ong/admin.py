from django.contrib import admin
from .models import DestaqueInicio, ConteudoSobre, Atividade, MembroEquipe

@admin.register(DestaqueInicio)
class DestaqueInicioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'subtitulo')

@admin.register(ConteudoSobre)
class ConteudoSobreAdmin(admin.ModelAdmin):
    list_display = ('titulo_secao',)

@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data')
    list_filter = ('data',)

@admin.register(MembroEquipe)
class MembroEquipeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cargo')