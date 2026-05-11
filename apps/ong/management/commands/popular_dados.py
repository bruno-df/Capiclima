"""
Management command para popular o banco de dados com os dados reais do CapiClima.
Uso: python manage.py popular_dados
"""
from datetime import date
from django.core.management.base import BaseCommand
from apps.ong.models import MembroEquipe, Atividade, ConfiguracaoSite


class Command(BaseCommand):
    help = 'Popula o banco de dados com os dados reais do CapiClima (equipe e atividades)'

    def handle(self, *args, **options):
        self.popular_equipe()
        self.popular_atividades()
        self.popular_config()
        self.stdout.write(self.style.SUCCESS('Dados populados com sucesso!'))

    def popular_equipe(self):
        membros = [
            {
                'nome': 'Gregório Teófilo',
                'cargo': 'Coordenador de Incidência e Representação',
                'bio': 'Ativista socioambiental, técnico em Meio Ambiente pelo Instituto Federal do Maranhão e recém-formado em Engenharia Sanitária e Ambiental pela Universidade Federal de Mato Grosso (UFMT). Pesquisador nas áreas de segurança hídrica e alimentar em comunidades ribeirinhas. Atua em movimentos socioambientais desde a adolescência. É duplamente latino-americano: nascido no Panamá, com raízes no Maranhão e no Mato Grosso. Mobiliza juventudes no enfrentamento as mudanças climáticas e na luta por justiça socioambiental.',
                'ordem': 1,
            },
            {
                'nome': 'Augusta Cesária',
                'cargo': 'Coordenadora de Mobilização e Engajamento',
                'bio': 'Ativista socioambiental, mulher travesti, pedagoga e graduanda em Filosofia pela UFMT. Atuou na coordenação do Diretório Central dos Estudantes (DCE/UFMT), coordena o Coletivo LGBTQIAPN+ Hend Santana e milita pelas pautas de educação, diversidade e justiça social. Foi representante do LabNarra – Laboratório de Narrativas Regionais do projeto Amazônia de Pé.',
                'ordem': 2,
            },
            {
                'nome': 'Vinícius Sanches',
                'cargo': 'Coordenador de Formação e Planejamento',
                'bio': 'Ativista dos direitos humanos, técnico em Informática pelo Instituto Federal de Rondônia (IFRO) e graduando em Serviço Social pela Universidade Federal de Mato Grosso (UFMT). Pesquisador na área da justiça social, com foco em saúde mental, justiça ambiental e efetivação dos direitos da infância e juventude. Desenvolve ações que articulam formação crítica, prática extensionista e compromisso ético-político com a defesa dos direitos sociais e ambientais.',
                'ordem': 3,
            },
            {
                'nome': 'Eduarda Almeida',
                'cargo': 'Coordenadora de Comunicação',
                'bio': 'Ativista socioambiental, técnica em Desenho de Construção Civil pelo IFMT e graduanda em Jornalismo pela Universidade Federal de Mato Grosso (UFMT). Pesquisadora nas áreas de sustentabilidade, juventudes e mudanças climáticas. Atua na comunicação popular, produzindo conteúdos informativos e engajando jovens por meio das redes sociais.',
                'ordem': 4,
            },
            {
                'nome': 'Vinicius Costa',
                'cargo': 'Coordenador de Captação de Recursos',
                'bio': 'Ativista socioambiental, técnico em Edificações pelo IFMT e graduando em Administração pela UFMT. Presidente da Liga Acadêmica de Sustentabilidade e Justiça Climática (LAJUSC), militante do movimento estudantil e integrante da equipe de jovens mobilizadores da VI Conferência Nacional Infantojuvenil pelo Meio Ambiente (MEC). Pesquisa justiça climática e representou as pautas brasileiras no European Forum Alpbach, na Áustria.',
                'ordem': 5,
            },
            {
                'nome': 'Lucas',
                'cargo': 'Coordenador de Articulação Territorial',
                'bio': 'Membro do coletivo reconhecido por sua destacada atuação e contribuição para as causas socioambientais. Recebeu moção de aplausos durante o 1º Seminário Estadual dos ODS de Mato Grosso.',
                'ordem': 6,
            },
        ]

        for m in membros:
            obj, created = MembroEquipe.objects.get_or_create(
                nome=m['nome'],
                defaults=m
            )
            status = 'CRIADO' if created else 'já existe'
            self.stdout.write(f"  Membro: {m['nome']} — {status}")

    def popular_atividades(self):
        atividades = [
            {
                'nome': 'Oficina "Direitos LGBTQIAPN+ e Crise Ambiental: Por uma Agenda Inclusiva na COP 30"',
                'data': date(2025, 6, 4),
                'local': 'ICHS – UFMT, Cuiabá - MT',
                'destaque': True,
                'descricao': 'A oficina integrou a programação da Virada Sustentável 2025 e foi organizada pelo Coletivo CapiClima, com o objetivo de promover uma reflexão interseccional sobre a crise climática, articulando as pautas de direitos LGBTQIAPN+ e justiça ambiental, visando uma agenda inclusiva para a COP 30.',
            },
            {
                'nome': 'Oficina de Formação para a Equipe Interdisciplinar da Defensoria Pública do Estado de Mato Grosso',
                'data': date(2025, 5, 23),
                'local': 'Defensoria Pública do Estado de Mato Grosso',
                'destaque': False,
                'descricao': 'A oficina teve como tema "Justiça Climática e Direitos Humanos: O papel da Defensoria Pública nas lutas por equidade ambiental", com o objetivo de aprofundar o debate sobre Justiça Climática e sua interface com os direitos humanos no contexto da atuação da Defensoria Pública.',
            },
            {
                'nome': 'Roda de Conversa "Juventudes Mato-Grossenses, Meio Ambiente e Justiça Climática"',
                'data': date(2025, 5, 21),
                'local': 'ADUFMAT - Cuiabá - MT',
                'destaque': True,
                'descricao': 'A roda de conversa integrou a programação do LabNarra – Programa Amazônia de Pé, mediada por Augusta Cesária. O objetivo foi criar um espaço de escuta e troca de experiências entre jovens universitários, promovendo reflexões sobre os desafios socioambientais na Amazônia e o protagonismo juvenil como agente de transformação.',
            },
            {
                'nome': 'Instagram como Ferramenta de Educação Popular',
                'data': date(2025, 1, 15),
                'local': 'Redes Sociais',
                'destaque': False,
                'descricao': 'A ação utilizou as redes sociais como meio de mobilização e conscientização sobre temas de justiça climática, ampliando o alcance das discussões ambientais e aproximando o público jovem das pautas socioambientais.',
            },
            {
                'nome': 'Seminário Nacional de Juventude, Meio Ambiente e Justiça Climática',
                'data': date(2024, 11, 21),
                'local': 'Brasília - DF',
                'destaque': True,
                'descricao': 'Representar o bioma Pantanal no Seminário Nacional de Juventude, Meio Ambiente e Justiça Climática, realizado pelo Ministério do Meio Ambiente e Mudança do Clima em Brasília. Essa participação marcou um divisor de águas na trajetória do coletivo.',
            },
            {
                'nome': 'Oficina "O Protagonismo da Juventude no Enfrentamento às Mudanças Climáticas"',
                'data': date(2024, 11, 8),
                'local': 'IFMT - Campus Cuiabá',
                'destaque': False,
                'descricao': 'A oficina foi organizada pelo Coletivo CapiClima com o objetivo de promover o protagonismo juvenil frente às questões ambientais, integrando ensino, pesquisa e extensão no âmbito dos Objetivos do Desenvolvimento Sustentável (ODS) da Agenda 2030.',
            },
            {
                'nome': '1º Seminário Estadual dos ODS de Mato Grosso',
                'data': date(2024, 6, 5),
                'local': 'UFMT - Cuiabá - MT',
                'destaque': False,
                'descricao': 'Participação no 1º Seminário Estadual dos Objetivos do Desenvolvimento Sustentável de Mato Grosso, com organização de banca de assinaturas para o Projeto de Lei Amazônia de Pé e atividades de educação popular.',
            },
            {
                'nome': 'Sarau "É Tempo de Caju" – Virada Cultural do Movimento Amazônia de Pé',
                'data': date(2024, 6, 5),
                'local': 'UFMT - Cuiabá - MT',
                'destaque': False,
                'descricao': 'Sarau artístico-cultural organizado pelo Coletivo CapiClima em parceria com o Movimento Amazônia de Pé. O evento valorizou a cultura como instrumento de mobilização social em defesa da Amazônia. Foram coletadas mais de 200 assinaturas para o Projeto de Lei Amazônia de Pé.',
            },
            {
                'nome': 'Webinário "O Papel da Juventude na Construção da Justiça Climática"',
                'data': date(2024, 10, 24),
                'local': 'Plataforma virtual Google Meet',
                'destaque': False,
                'descricao': 'Webinário promovido pelo Coletivo CapiClima com o objetivo de ampliar o debate sobre a participação juvenil na agenda socioambiental, com ênfase na justiça climática. Reuniu cerca de 30 participantes entre estudantes, pesquisadores, ativistas e membros de organizações sociais.',
            },
            {
                'nome': 'Ação em Defesa das Árvores Centenárias em Chapada dos Guimarães',
                'data': date(2024, 7, 12),
                'local': 'Chapada dos Guimarães - MT',
                'destaque': False,
                'descricao': 'Atividade promovida como resposta à tentativa de corte de árvores centenárias em Chapada dos Guimarães. A ação defendeu o patrimônio ambiental e histórico da região, mobilizando a sociedade civil. Ganhou repercussão no canal Olhar Direto (200 mil seguidores).',
            },
            {
                'nome': 'Roda de Conversa "Juventudes, Meio Ambiente e Justiça Climática"',
                'data': date(2024, 6, 12),
                'local': 'UFMT - Cuiabá - MT',
                'destaque': False,
                'descricao': 'Roda de conversa promovida em parceria com a Virada Sustentável de Mato Grosso – Edição 2024. Reuniu cerca de 15 estudantes da UFMT para troca de experiências e reflexão crítica sobre os impactos das mudanças climáticas nas juventudes.',
            },
        ]

        for a in atividades:
            obj, created = Atividade.objects.get_or_create(
                nome=a['nome'],
                defaults=a
            )
            status = 'CRIADO' if created else 'já existe'
            self.stdout.write(f"  Atividade: {a['nome'][:60]}... — {status}")

    def popular_config(self):
        ConfiguracaoSite.load()
        self.stdout.write("  ConfiguracaoSite — OK")
