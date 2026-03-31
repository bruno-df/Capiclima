from django.db import models

# Aba: Início
class DestaqueInicio(models.Model):
    titulo = models.CharField("Título do Banner", max_length=100)
    subtitulo = models.CharField("Subtítulo/Frase", max_length=200, blank=True)
    imagem = models.ImageField("Imagem de Destaque", upload_to='inicio/')

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Destaque de Início"
        verbose_name_plural = "Destaques de Início"

# Aba: Sobre
class ConteudoSobre(models.Model):
    titulo_secao = models.CharField("Título da Seção", max_length=100)
    texto_informativo = models.TextField("Texto sobre a ONG")
    imagem = models.ImageField("Foto Informativa", upload_to='sobre/')

    def __str__(self):
        return self.titulo_secao

    class Meta:
        verbose_name = "Conteúdo Sobre"
        verbose_name_plural = "Conteúdos Sobre"

# Aba: Atividades
class Atividade(models.Model):
    nome = models.CharField("Nome da Atividade", max_length=150)
    data = models.DateField("Data de Realização")
    descricao = models.TextField("Descrição da Atividade")
    imagem = models.ImageField("Foto da Atividade", upload_to='atividades/')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Atividade"
        verbose_name_plural = "Atividades"

# Aba: Equipe (Nova!)
class MembroEquipe(models.Model):
    nome = models.CharField("Nome do Integrante", max_length=100)
    cargo = models.CharField("Cargo/Função", max_length=100)
    foto = models.ImageField("Foto de Perfil", upload_to='equipe/')
    linkedin = models.URLField("Link do LinkedIn", blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - {self.cargo}"

    class Meta:
        verbose_name = "Membro da Equipe"
        verbose_name_plural = "Membros da Equipe"