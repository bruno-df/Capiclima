"""
Management command para popular o banco com dados iniciais do CMS.
Idempotente — pode ser executado multiplas vezes sem duplicar registros.

Uso: python manage.py seed_data
"""
from datetime import date

from django.core.management.base import BaseCommand

from apps.ong.models import (
    Atividade,
    MembroEquipe,
    Opportunity,
    SiteConfig,
    SiteSection,
)
from apps.ong.permissions import sync_cms_groups


class Command(BaseCommand):
    help = "Popula o banco com dados iniciais do CMS CapiClima (idempotente)"

    def handle(self, *args, **options):
        self._seed_config()
        self._seed_groups()
        self._seed_sections()
        self._seed_equipe()
        self._seed_atividades()
        self._seed_oportunidades()
        self.stdout.write(self.style.SUCCESS("Seed concluido com sucesso!"))

    # ------------------------------------------------------------------ #
    # Configuracao global
    # ------------------------------------------------------------------ #
    def _seed_config(self):
        config = SiteConfig.load()
        self.stdout.write(f"  SiteConfig: {config.nome_site} — OK")

    # ------------------------------------------------------------------ #
    # Grupos e permissoes
    # ------------------------------------------------------------------ #
    def _seed_groups(self):
        colaboradores, admins = sync_cms_groups()
        self.stdout.write(
            f"  Grupo Colaboradores: {colaboradores.permissions.count()} permissoes"
        )
        self.stdout.write(
            f"  Grupo Admin: {admins.permissions.count()} permissoes"
        )

    # ------------------------------------------------------------------ #
    # Secoes editaveis do site
    # ------------------------------------------------------------------ #
    def _seed_sections(self):
        sections = [
            {
                "nome": "Home — Juventudes em Acao",
                "slug": "home-juventudes",
                "titulo": "Juventudes em Ação",
                "texto_principal": "<p>Conheça as iniciativas que estamos desenvolvendo pelo meio ambiente e pela educação.</p>",
                "ordem": 1,
            },
            {
                "nome": "Home — Parceiros",
                "slug": "home-parceiros",
                "titulo": "Nossos Parceiros",
                "texto_principal": "",
                "ordem": 2,
            },
            {
                "nome": "Home — CTA",
                "slug": "home-cta",
                "titulo": "Quer fazer a diferença?",
                "texto_principal": "<p>Junte-se ao CapiClima e seja parte da transformação climática!</p>",
                "ordem": 3,
            },
            {
                "nome": "Apoie — Voluntariado",
                "slug": "apoie-voluntariado",
                "titulo": "Voluntariado",
                "texto_principal": "<p>Doe seu tempo e expertise! Conheça as oportunidades de voluntariado no CapiClima.</p>",
                "botao_texto": "Ver Oportunidades",
                "botao_url": "/oportunidades/",
                "ordem": 1,
            },
            {
                "nome": "Apoie — Doacao Financeira",
                "slug": "apoie-doacao",
                "titulo": "Doação Financeira",
                "texto_principal": "<p>Sua doação financia oficinas, materiais educativos e eventos comunitários.</p>",
                "ordem": 2,
            },
            {
                "nome": "Apoie — Parcerias",
                "slug": "apoie-parcerias",
                "titulo": "Parcerias Empresariais",
                "texto_principal": "<p>Sua empresa pode apoiar nossas iniciativas através de parcerias estratégicas e patrocínios.</p>",
                "ordem": 3,
            },
            {
                "nome": "Apoie — Compartilhe",
                "slug": "apoie-compartilhe",
                "titulo": "Compartilhe",
                "texto_principal": "<p>Espalhe a palavra! Compartilhe nosso trabalho nas redes sociais e com seus amigos.</p>",
                "ordem": 4,
            },
        ]
        for s in sections:
            obj, created = SiteSection.objects.get_or_create(
                slug=s["slug"], defaults=s
            )
            status = "CRIADO" if created else "ja existe"
            self.stdout.write(f"  Secao: {s['nome']} — {status}")

    # ------------------------------------------------------------------ #
    # Equipe
    # ------------------------------------------------------------------ #
    def _seed_equipe(self):
        membros = [
            {
                "nome": "Gregório Teófilo",
                "cargo": "Coordenador de Incidência e Representação",
                "foto_local": "images/gestao/Gregorio.jpg",
                "bio": "Ativista socioambiental, técnico em Meio Ambiente pelo IFMA e engenheiro sanitarista e ambiental pela UFMT. Pesquisador em segurança hídrica e alimentar.",
                "ordem": 1,
            },
            {
                "nome": "Augusta Cesária",
                "cargo": "Coordenadora de Mobilização e Engajamento",
                "foto_local": "images/gestao/Augusta.jpg",
                "bio": "Ativista socioambiental, mulher travesti, pedagoga e graduanda em Filosofia pela UFMT. Coordena o Coletivo LGBTQIAPN+ Hend Santana.",
                "ordem": 2,
            },
            {
                "nome": "Vinícius Sanches",
                "cargo": "Coordenador de Formação e Planejamento",
                "foto_local": "images/gestao/ViniciusSanches.jpg",
                "bio": "Ativista dos direitos humanos, técnico em Informática pelo IFRO e graduando em Serviço Social pela UFMT.",
                "ordem": 3,
            },
            {
                "nome": "Eduarda Almeida",
                "cargo": "Coordenadora de Comunicação",
                "foto_local": "images/gestao/Eduarda.jpg",
                "bio": "Ativista socioambiental, técnica em Desenho de Construção Civil pelo IFMT e graduanda em Jornalismo pela UFMT.",
                "ordem": 4,
            },
            {
                "nome": "Vinicius Costa",
                "cargo": "Coordenador de Captação de Recursos",
                "foto_local": "images/gestao/ViniciusCosta.jpeg",
                "bio": "Ativista socioambiental, técnico em Edificações pelo IFMT e graduando em Administração pela UFMT. Presidente da LAJUSC.",
                "ordem": 5,
            },
            {
                "nome": "Lucas Silva",
                "cargo": "Coordenador de Articulação Territorial",
                "foto_local": "images/gestao/Lucas.jpeg",
                "bio": "Membro do coletivo reconhecido por sua atuação socioambiental. Recebeu moção de aplausos no 1º Seminário Estadual dos ODS de MT.",
                "ordem": 6,
            },
        ]
        for m in membros:
            obj, created = MembroEquipe.objects.get_or_create(
                nome=m["nome"], defaults=m
            )
            status = "CRIADO" if created else "ja existe"
            self.stdout.write(f"  Membro: {m['nome']} — {status}")

    # ------------------------------------------------------------------ #
    # Atividades
    # ------------------------------------------------------------------ #
    def _seed_atividades(self):
        atividades = [
            {
                "nome": 'Oficina "Direitos LGBTQIAPN+ e Crise Ambiental: Por uma Agenda Inclusiva na COP 30"',
                "tipo": "Oficina",
                "data": date(2025, 6, 4),
                "local": "ICHS – UFMT, Cuiabá - MT",
                "destaque": True,
                "descricao": "Oficina integrada à Virada Sustentável 2025 com reflexão interseccional sobre crise climática e direitos LGBTQIAPN+.",
            },
            {
                "nome": "Oficina de Formação para a Equipe Interdisciplinar da Defensoria Pública do Estado de Mato Grosso",
                "tipo": "Oficina",
                "data": date(2025, 5, 23),
                "local": "Defensoria Pública do Estado de Mato Grosso",
                "destaque": False,
                "descricao": "Tema: Justiça Climática e Direitos Humanos — o papel da Defensoria Pública nas lutas por equidade ambiental.",
            },
            {
                "nome": 'Roda de Conversa "Juventudes Mato-Grossenses, Meio Ambiente e Justiça Climática"',
                "tipo": "Roda de Conversa",
                "data": date(2025, 5, 21),
                "local": "ADUFMAT - Cuiabá - MT",
                "destaque": True,
                "descricao": "Integrou a programação do LabNarra — Programa Amazônia de Pé, mediada por Augusta Cesária.",
            },
            {
                "nome": "Instagram como Ferramenta de Educação Popular",
                "tipo": "Acao Digital",
                "data": date(2025, 1, 15),
                "local": "Redes Sociais",
                "destaque": False,
                "descricao": "Uso das redes sociais como meio de mobilização e conscientização sobre justiça climática.",
            },
            {
                "nome": "Seminário Nacional de Juventude, Meio Ambiente e Justiça Climática",
                "tipo": "Seminario",
                "data": date(2024, 11, 21),
                "local": "Brasília - DF",
                "destaque": True,
                "descricao": "Representação do bioma Pantanal no Seminário Nacional, realizado pelo MMA em Brasília.",
            },
            {
                "nome": 'Oficina "O Protagonismo da Juventude no Enfrentamento às Mudanças Climáticas"',
                "tipo": "Oficina",
                "data": date(2024, 11, 8),
                "local": "IFMT - Campus Cuiabá",
                "destaque": False,
                "descricao": "Promoção do protagonismo juvenil frente às questões ambientais, integrando ensino, pesquisa e extensão.",
            },
            {
                "nome": "1º Seminário Estadual dos ODS de Mato Grosso",
                "tipo": "Seminario",
                "data": date(2024, 6, 5),
                "local": "UFMT - Cuiabá - MT",
                "destaque": False,
                "descricao": "Participação com banca de assinaturas para o PL Amazônia de Pé e atividades de educação popular.",
            },
            {
                "nome": 'Sarau "É Tempo de Caju" – Virada Cultural do Movimento Amazônia de Pé',
                "tipo": "Evento Cultural",
                "data": date(2024, 6, 5),
                "local": "UFMT - Cuiabá - MT",
                "destaque": False,
                "descricao": "Sarau artístico-cultural em parceria com o Movimento Amazônia de Pé. Mais de 200 assinaturas coletadas.",
            },
            {
                "nome": 'Webinário "O Papel da Juventude na Construção da Justiça Climática"',
                "tipo": "Webinario",
                "data": date(2024, 10, 24),
                "local": "Plataforma virtual Google Meet",
                "destaque": False,
                "descricao": "Webinário com cerca de 30 participantes entre estudantes, pesquisadores e ativistas.",
            },
            {
                "nome": "Ação em Defesa das Árvores Centenárias em Chapada dos Guimarães",
                "tipo": "Mobilizacao",
                "data": date(2024, 7, 12),
                "local": "Chapada dos Guimarães - MT",
                "destaque": False,
                "descricao": "Resposta à tentativa de corte de árvores centenárias. Repercussão no canal Olhar Direto.",
            },
            {
                "nome": 'Roda de Conversa "Juventudes, Meio Ambiente e Justiça Climática"',
                "tipo": "Roda de Conversa",
                "data": date(2024, 6, 12),
                "local": "UFMT - Cuiabá - MT",
                "destaque": False,
                "descricao": "Parceria com a Virada Sustentável de MT 2024. Cerca de 15 estudantes da UFMT participaram.",
            },
        ]
        for a in atividades:
            obj, created = Atividade.objects.get_or_create(
                nome=a["nome"], defaults=a
            )
            status = "CRIADO" if created else "ja existe"
            self.stdout.write(f"  Atividade: {a['nome'][:60]}... — {status}")

    # ------------------------------------------------------------------ #
    # Oportunidades
    # ------------------------------------------------------------------ #
    def _seed_oportunidades(self):
        oportunidades = [
            {
                "titulo": "Ação de limpeza em parceria com a Asmat",
                "descricao": "<p>Ação voluntária de limpeza ambiental em parceria com a Asmat. Detalhes a definir.</p>",
                "link": "https://forms.gle/exemplo1",
                "data_inicio": date(2025, 10, 1),
                "data_fim": date(2025, 10, 31),
                "ordem": 1,
            },
            {
                "titulo": "Oficina de reflorestamento",
                "descricao": "<p>Oficina prática de reflorestamento com espécies nativas do Cerrado. Detalhes a definir.</p>",
                "link": "https://forms.gle/exemplo2",
                "data_inicio": date(2025, 10, 1),
                "data_fim": date(2025, 10, 31),
                "ordem": 2,
            },
            {
                "titulo": "Atividade de educação ambiental com ensino médio",
                "descricao": "<p>Atividade de educação ambiental voltada para estudantes do ensino médio. Detalhes a definir.</p>",
                "link": "https://forms.gle/exemplo3",
                "data_inicio": date(2025, 10, 1),
                "data_fim": date(2025, 10, 31),
                "ordem": 3,
            },
            {
                "titulo": "COP 30 em Belém do Pará",
                "descricao": "<p>Participação e mobilização na COP 30 em Belém. Detalhes a definir.</p>",
                "link": "https://forms.gle/exemplo4",
                "data_inicio": date(2025, 11, 1),
                "data_fim": date(2025, 11, 30),
                "ordem": 4,
            },
            {
                "titulo": "Confraternização de fim de ano",
                "descricao": "<p>Confraternização de fim de ano do Coletivo CapiClima. Detalhes a definir.</p>",
                "link": "https://forms.gle/exemplo5",
                "data_inicio": date(2025, 12, 1),
                "data_fim": date(2025, 12, 31),
                "ordem": 5,
            },
        ]
        for o in oportunidades:
            obj, created = Opportunity.objects.get_or_create(
                titulo=o["titulo"], defaults=o
            )
            status = "CRIADO" if created else "ja existe"
            self.stdout.write(f"  Oportunidade: {o['titulo']} — {status}")
