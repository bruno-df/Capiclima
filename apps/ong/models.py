from django.db import models
from cloudinary.models import CloudinaryField
from django_ckeditor_5.fields import CKEditor5Field


# ============================================
# Model: Destaque de Início (Banner da Home)
# ============================================
class DestaqueInicio(models.Model):
    titulo = models.CharField("Título do Banner", max_length=100)
    subtitulo = models.CharField("Subtítulo/Frase", max_length=200, blank=True)
    imagem = CloudinaryField("Imagem de Destaque", folder='inicio/', blank=True, null=True)
    ativo = models.BooleanField("Ativo?", default=True, help_text="Desmarque para ocultar este destaque do site.")
    ordem = models.PositiveIntegerField("Ordem de Exibição", default=0, help_text="Menor número aparece primeiro.")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Destaque de Início"
        verbose_name_plural = "Destaques de Início"
        ordering = ['ordem']


# ============================================
# Model: Conteúdo Sobre (Seções da página Sobre)
# ============================================
class ConteudoSobre(models.Model):
    titulo_secao = models.CharField("Título da Seção", max_length=100)
    texto_informativo = CKEditor5Field("Texto sobre a ONG", config_name='default')
    imagem = CloudinaryField("Foto Informativa", folder='sobre/', blank=True, null=True)
    icone = models.CharField(
        "Ícone Font Awesome",
        max_length=50,
        blank=True,
        help_text="Ex: fas fa-leaf, fas fa-users, fas fa-globe"
    )
    ordem = models.PositiveIntegerField("Ordem de Exibição", default=0)

    def __str__(self):
        return self.titulo_secao

    class Meta:
        verbose_name = "Conteúdo Sobre"
        verbose_name_plural = "Conteúdos Sobre"
        ordering = ['ordem']


# ============================================
# Model: Atividade (Eventos e ações realizadas)
# ============================================
class Atividade(models.Model):
    nome = models.CharField("Nome da Atividade", max_length=150)
    data = models.DateField("Data de Realização")
    descricao = CKEditor5Field("Descrição da Atividade", config_name='default')
    imagem = CloudinaryField("Foto da Atividade", folder='atividades/', blank=True, null=True)
    imagem_local = models.CharField(
        "Imagem Local (fallback)",
        max_length=200,
        blank=True,
        help_text="Caminho relativo em static/. Ex: images/atividades/2024/atividade-012024.jpeg"
    )
    local = models.CharField("Local", max_length=200, blank=True, help_text="Ex: Cuiabá, MT")
    destaque = models.BooleanField(
        "Destacar na página inicial?",
        default=False,
        help_text="Marque para exibir esta atividade na página inicial."
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Atividade"
        verbose_name_plural = "Atividades"
        ordering = ['-data']


# ============================================
# Model: Membro da Equipe
# ============================================
class MembroEquipe(models.Model):
    nome = models.CharField("Nome do Integrante", max_length=100)
    cargo = models.CharField("Cargo/Função", max_length=100)
    foto = CloudinaryField("Foto de Perfil", folder='equipe/', blank=True, null=True)
    foto_local = models.CharField(
        "Foto Local (fallback)",
        max_length=200,
        blank=True,
        help_text="Caminho relativo em static/. Ex: images/gestao/Gregorio.jpg"
    )
    bio = models.TextField("Biografia Curta", blank=True, help_text="Uma breve descrição sobre o membro.")
    linkedin = models.URLField("Link do LinkedIn", blank=True, null=True)
    ordem = models.PositiveIntegerField("Ordem de Exibição", default=0)

    def __str__(self):
        return f"{self.nome} - {self.cargo}"

    class Meta:
        verbose_name = "Membro da Equipe"
        verbose_name_plural = "Membros da Equipe"
        ordering = ['ordem']


# ============================================
# Model: Configuração do Site (Singleton)
# Permite que a equipe gerencie informações
# globais do site pelo painel admin.
# ============================================
class ConfiguracaoSite(models.Model):
    # Identidade
    nome_site = models.CharField("Nome do Site", max_length=100, default="CapiClima")
    slogan = models.CharField("Slogan", max_length=200, blank=True, default="Juventude, Educação e Meio Ambiente")
    logo = CloudinaryField("Logo do Site", folder='config/', blank=True, null=True)
    favicon = CloudinaryField("Favicon", folder='config/', blank=True, null=True)

    # Contato
    email = models.EmailField("E-mail de Contato", blank=True, default="coletivocapiclima@gmail.com")
    telefone = models.CharField("Telefone", max_length=20, blank=True, default="(65) 9 9919-4450")
    whatsapp = models.CharField(
        "Número WhatsApp (com DDI)",
        max_length=20,
        blank=True,
        default="5565999194450",
        help_text="Apenas números, com DDI. Ex: 5565999194450"
    )
    endereco = models.TextField("Endereço", blank=True)

    # Redes Sociais
    instagram_url = models.URLField("Link do Instagram", blank=True, default="https://www.instagram.com/capiclima")
    twitter_url = models.URLField("Link do Twitter/X", blank=True)
    facebook_url = models.URLField("Link do Facebook", blank=True)
    youtube_url = models.URLField("Link do YouTube", blank=True)

    # Doações
    chave_pix = models.CharField("Chave Pix", max_length=100, blank=True, default="coletivocapiclima@gmail.com")
    qrcode_pix = CloudinaryField("QR Code Pix", folder='config/', blank=True, null=True)

    # Rodapé
    texto_rodape = models.CharField(
        "Texto do Rodapé",
        max_length=200,
        blank=True,
        default="Todos os direitos reservados."
    )

    def __str__(self):
        return self.nome_site

    class Meta:
        verbose_name = "Configuração do Site"
        verbose_name_plural = "Configuração do Site"

    def save(self, *args, **kwargs):
        """Singleton: garante que só exista 1 registro."""
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Impede a exclusão do registro único."""
        pass

    @classmethod
    def load(cls):
        """Carrega ou cria a configuração do site."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj