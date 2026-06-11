from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone

from cloudinary.models import CloudinaryField
from django_ckeditor_5.fields import CKEditor5Field


ALLOWED_IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]


def image_extension_validator(value):
    if not value or isinstance(value, bool):
        return

    name = getattr(value, "name", "")

    if not name:
        return

    extension = name.split(".")[-1].lower()

    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            f"Formato de imagem inválido. Use: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}."
        )


class SiteSection(models.Model):
    nome = models.CharField("Nome interno", max_length=120)
    slug = models.SlugField("Slug", max_length=140, unique=True)
    titulo = models.CharField("Titulo exibido", max_length=160, blank=True)
    texto_principal = CKEditor5Field("Texto principal", config_name="default", blank=True)
    imagem = CloudinaryField(
        "Imagem",
        folder="sections/",
        blank=True,
        null=True,
        validators=[image_extension_validator],
    )
    botao_texto = models.CharField("Texto do botao", max_length=80, blank=True)
    botao_url = models.CharField("URL do botao", max_length=250, blank=True)
    ordem = models.PositiveIntegerField("Ordem de exibicao", default=0)
    ativo = models.BooleanField("Ativo?", default=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Secao do Site"
        verbose_name_plural = "Secoes do Site"
        ordering = ["ordem", "nome"]


class Opportunity(models.Model):
    titulo = models.CharField("Titulo", max_length=180)
    descricao = CKEditor5Field("Descricao", config_name="default")
    link = models.URLField("Link para inscricao", blank=True)
    data_inicio = models.DateField("Data de inicio", blank=True, null=True)
    data_fim = models.DateField("Data de fim", blank=True, null=True)
    ativo = models.BooleanField("Ativo?", default=True)
    ordem = models.PositiveIntegerField("Ordem de exibicao", default=0)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    def __str__(self):
        return self.titulo

    @property
    def esta_aberta(self):
        hoje = timezone.localdate()
        return self.ativo and (self.data_fim is None or self.data_fim >= hoje)

    @classmethod
    def abertas(cls):
        hoje = timezone.localdate()
        return cls.objects.filter(ativo=True).filter(
            Q(data_fim__isnull=True) | Q(data_fim__gte=hoje)
        )

    class Meta:
        verbose_name = "Oportunidade"
        verbose_name_plural = "Oportunidades"
        ordering = ["ordem", "data_inicio", "data_fim", "titulo"]


class DestaqueInicio(models.Model):
    titulo = models.CharField("Titulo do Banner", max_length=100)
    subtitulo = models.CharField("Subtitulo/Frase", max_length=200, blank=True)
    imagem = CloudinaryField(
        "Imagem de Destaque",
        folder="inicio/",
        blank=True,
        null=True,
        validators=[image_extension_validator],
    )
    texto_botao = models.CharField(
        "Texto do botão",
        max_length=80,
        blank=True,
        default="",
        help_text="Ex: Saiba mais, Inscreva-se, Ver atividade.",
    )
    link_botao = models.CharField(
        "Link do botão",
        max_length=250,
        blank=True,
        default="",
        help_text="Pode ser um link interno, como /atividades/, ou externo.",
    )
    abrir_nova_aba = models.BooleanField(
        "Abrir link em nova aba?",
        default=False,
    )
    ativo = models.BooleanField(
        "Ativo?",
        default=True,
        help_text="Desmarque para ocultar este destaque do site.",
    )
    ordem = models.PositiveIntegerField(
        "Ordem de exibicao",
        default=0,
        help_text="Menor numero aparece primeiro.",
    )

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Destaque de Inicio"
        verbose_name_plural = "Destaques de Inicio"
        ordering = ["ordem"]


class ConteudoSobre(models.Model):
    titulo_secao = models.CharField("Titulo da Secao", max_length=100)
    texto_informativo = CKEditor5Field("Texto sobre a ONG", config_name="default")
    imagem = CloudinaryField(
        "Foto Informativa",
        folder="sobre/",
        blank=True,
        null=True,
        validators=[image_extension_validator],
    )
    icone = models.CharField(
        "Icone Font Awesome",
        max_length=50,
        blank=True,
        help_text="Ex: fas fa-leaf, fas fa-users, fas fa-globe",
    )
    ordem = models.PositiveIntegerField("Ordem de exibicao", default=0)

    def __str__(self):
        return self.titulo_secao

    class Meta:
        verbose_name = "Conteudo Sobre"
        verbose_name_plural = "Conteudos Sobre"
        ordering = ["ordem"]


class Atividade(models.Model):
    nome = models.CharField("Nome da Atividade", max_length=150)
    tipo = models.CharField("Tipo da Atividade", max_length=80, blank=True)
    data = models.DateField("Data de Realizacao")
    horario = models.CharField("Horario", max_length=80, blank=True)
    descricao = CKEditor5Field("Descricao da Atividade", config_name="default")
    imagem = CloudinaryField(
        "Foto da Atividade",
        folder="atividades/",
        blank=True,
        null=True,
        validators=[image_extension_validator],
    )
    imagem_local = models.CharField(
        "Imagem Local (fallback)",
        max_length=200,
        blank=True,
        help_text="Caminho relativo em static/. Ex: images/atividades/2024/atividade-012024.jpeg",
    )
    local = models.CharField("Local", max_length=200, blank=True, help_text="Ex: Cuiaba, MT")
    destaque = models.BooleanField(
        "Destacar na pagina inicial?",
        default=False,
        help_text="Marque para exibir esta atividade na pagina inicial.",
    )
    ativo = models.BooleanField("Ativo?", default=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Atividade"
        verbose_name_plural = "Atividades"
        ordering = ["-data"]


class MembroEquipe(models.Model):
    nome = models.CharField("Nome do Integrante", max_length=100)
    cargo = models.CharField("Cargo/Funcao", max_length=100)
    foto = CloudinaryField(
        "Foto de Perfil",
        folder="equipe/",
        blank=True,
        null=True,
        validators=[image_extension_validator],
    )
    foto_local = models.CharField(
        "Foto Local (fallback)",
        max_length=200,
        blank=True,
        help_text="Caminho relativo em static/. Ex: images/gestao/Gregorio.jpg",
    )
    bio = models.TextField("Biografia Curta", blank=True)
    instagram = models.URLField("Link do Instagram", blank=True, null=True)
    linkedin = models.URLField("Link do LinkedIn", blank=True, null=True)
    ordem = models.PositiveIntegerField("Ordem de exibicao", default=0)

    def __str__(self):
        return f"{self.nome} - {self.cargo}"

    class Meta:
        verbose_name = "Membro da Equipe"
        verbose_name_plural = "Membros da Equipe"
        ordering = ["ordem"]


class SingletonMixin(models.Model):
    """Mixin para modelos que devem ter exatamente 1 registro."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return None

    @classmethod
    def load(cls):
        obj, _created = cls.objects.get_or_create(pk=1)
        return obj


class SiteConfig(SingletonMixin):
    nome_site = models.CharField("Nome do Site", max_length=100, default="CapiClima")
    slogan = models.CharField(
        "Slogan",
        max_length=200,
        blank=True,
        default="Juventude, Educacao e Meio Ambiente",
    )
    logo = CloudinaryField(
        "Logo do Site",
        folder="config/",
        blank=True,
        null=True,
        validators=[image_extension_validator],
        help_text="Logo principal do site. Recomendado: PNG com fundo transparente.",
    )
    favicon = CloudinaryField(
        "Favicon",
        folder="config/",
        blank=True,
        null=True,
        validators=[image_extension_validator],
        help_text="Ícone exibido na aba do navegador. Recomendado: 32×32px.",
    )
    email = models.EmailField(
        "E-mail de Contato",
        blank=True,
        default="coletivocapiclima@gmail.com",
    )
    telefone = models.CharField("Telefone", max_length=20, blank=True, default="(65) 9 9919-4450")
    whatsapp = models.CharField(
        "Numero WhatsApp (com DDI)",
        max_length=20,
        blank=True,
        default="5565999194450",
        help_text="Apenas numeros, com DDI. Ex: 5565999194450",
    )
    endereco = models.TextField("Endereco", blank=True)
    instagram_url = models.URLField(
        "Link do Instagram",
        blank=True,
        default="https://www.instagram.com/capiclima",
    )
    twitter_url = models.URLField("Link do Twitter/X", blank=True)
    facebook_url = models.URLField("Link do Facebook", blank=True)
    youtube_url = models.URLField("Link do YouTube", blank=True)
    chave_pix = models.CharField(
        "Chave Pix",
        max_length=100,
        blank=True,
        default="coletivocapiclima@gmail.com",
        help_text="Chave Pix para doações (e-mail, CPF, telefone ou aleatória).",
    )
    qrcode_pix = CloudinaryField(
        "QR Code Pix",
        folder="config/",
        blank=True,
        null=True,
        validators=[image_extension_validator],
        help_text="Imagem do QR Code para pagamento via Pix.",
    )
    texto_rodape = models.CharField(
        "Texto do Rodape",
        max_length=200,
        blank=True,
        default="Todos os direitos reservados.",
    )

    def __str__(self):
        return self.nome_site

    class Meta:
        verbose_name = "Configuracao do Site"
        verbose_name_plural = "Configuracao do Site"




class SecaoHome(SingletonMixin):
    """Conteúdo editável da página inicial."""

    titulo_principal = models.CharField(
        "Título principal (hero)", max_length=160, blank=True,
        help_text="Título exibido no banner principal da home.",
    )
    subtitulo = models.CharField(
        "Subtítulo (hero)", max_length=250, blank=True,
        help_text="Frase complementar abaixo do título principal.",
    )
    imagem_banner = CloudinaryField(
        "Imagem do banner",
        folder="home/",
        blank=True,
        null=True,
        validators=[image_extension_validator],
        help_text="Imagem de fundo do hero. Recomendado: 1920×800px.",
    )

    texto_juventudes = CKEditor5Field(
        "Texto — Juventudes em Ação", config_name="default", blank=True,
        help_text="Texto da seção 'Juventudes em Ação' na home.",
    )
    titulo_juventudes = models.CharField(
        "Título — Juventudes em Ação", max_length=160, blank=True,
        default="Juventudes em Ação",
    )
    imagem_juventudes = CloudinaryField(
        "Imagem — Juventudes",
        folder="home/",
        blank=True,
        null=True,
        validators=[image_extension_validator],
    )

    titulo_parceiros = models.CharField(
        "Título — Parceiros", max_length=160, blank=True,
        default="Nossos Parceiros",
    )
    texto_parceiros = CKEditor5Field(
        "Texto — Parceiros", config_name="default", blank=True,
    )
    imagem_parceiros = CloudinaryField(
        "Imagem — Parceiros",
        folder="home/",
        blank=True,
        null=True,
        validators=[image_extension_validator],
        help_text="Logotipos dos parceiros/apoiadores.",
    )

    titulo_cta = models.CharField(
        "Título — CTA", max_length=160, blank=True,
        default="Quer fazer a diferença?",
        help_text="Chamada para ação no final da home.",
    )
    texto_cta = CKEditor5Field(
        "Texto — CTA", config_name="default", blank=True,
    )
    link_cta = models.CharField(
        "URL do botão CTA", max_length=250, blank=True,
        help_text="Link do botão principal da CTA.",
    )

    def __str__(self):
        return "Página Inicial"

    class Meta:
        verbose_name = "Página Inicial"
        verbose_name_plural = "Página Inicial"


class SecaoSobre(SingletonMixin):
    """Conteúdo editável da página Sobre."""

    titulo = models.CharField(
        "Título da página", max_length=160, blank=True,
        default="Sobre o CapiClima",
    )
    texto_principal = CKEditor5Field(
        "Texto principal", config_name="default", blank=True,
        help_text="Texto institucional 'Quem Somos', missão, visão.",
    )
    imagem = CloudinaryField(
        "Imagem institucional",
        folder="sobre/",
        blank=True,
        null=True,
        validators=[image_extension_validator],
    )
    missao = CKEditor5Field(
        "Missão", config_name="default", blank=True,
    )
    visao = CKEditor5Field(
        "Visão", config_name="default", blank=True,
    )
    valores = CKEditor5Field(
        "Valores", config_name="default", blank=True,
    )

    def __str__(self):
        return "Página Sobre"

    class Meta:
        verbose_name = "Página Sobre"
        verbose_name_plural = "Página Sobre"


class SecaoApoie(SingletonMixin):
    """Conteúdo editável da página Apoie."""

    texto_voluntariado = CKEditor5Field(
        "Texto — Voluntariado", config_name="default", blank=True,
        help_text="Descrição da seção de voluntariado.",
    )
    link_voluntariado = models.CharField(
        "Link — Voluntariado", max_length=250, blank=True,
        default="/oportunidades/",
        help_text="URL do botão de voluntariado.",
    )
    texto_doacao = CKEditor5Field(
        "Texto — Doação", config_name="default", blank=True,
        help_text="Descrição da seção de doação financeira.",
    )
    link_doacao = models.CharField(
        "Link — Doação", max_length=250, blank=True,
        help_text="URL do botão de doação (opcional).",
    )
    texto_parcerias = CKEditor5Field(
        "Texto — Parcerias", config_name="default", blank=True,
        help_text="Descrição da seção de parcerias empresariais.",
    )
    link_parcerias = models.CharField(
        "Link — Parcerias", max_length=250, blank=True,
        help_text="URL do botão de parcerias (opcional).",
    )
    texto_compartilhe = CKEditor5Field(
        "Texto — Compartilhe", config_name="default", blank=True,
        help_text="Descrição da seção 'Compartilhe'.",
    )

    def __str__(self):
        return "Página Apoie"

    class Meta:
        verbose_name = "Página Apoie"
        verbose_name_plural = "Página Apoie"


# Backwards-compatible import name used by the partial migration already present.
ConfiguracaoSite = SiteConfig
