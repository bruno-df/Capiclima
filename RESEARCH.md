# Research - Migracao CapiClima para CMS Django

Data da pesquisa: 2026-06-08

## Estado atual encontrado

O repositorio ja contem uma migracao Django parcial, alem do site antigo preservado em `templates_old/`.

- Backend existente: projeto Django `capiclima` com app `apps.ong`.
- Banco local: `db.sqlite3` ignorado pelo Git, com 11 atividades, 6 membros e 1 configuracao.
- Django instalado localmente: 6.0.5; `requirements.txt` aponta `django==6.0.3`.
- Objetivo do AGENTS.md: Django 5.x, CMS via admin, oportunidades dinamicas, permissao por grupos, uploads validados e documentos finais.
- `python manage.py check` executou sem erros antes de qualquer alteracao de codigo.

## Estrutura de pastas atual

```text
.
|-- AGENTS.md
|-- manage.py
|-- requirements.txt
|-- capiclima/
|   |-- settings.py
|   |-- urls.py
|   |-- asgi.py
|   `-- wsgi.py
|-- apps/
|   `-- ong/
|       |-- admin.py
|       |-- apps.py
|       |-- context_processors.py
|       |-- models.py
|       |-- tests.py
|       |-- urls.py
|       |-- views.py
|       |-- migrations/
|       `-- management/commands/popular_dados.py
|-- templates/
|   |-- base.html
|   |-- includes/
|   |   |-- footer.html
|   |   |-- navbar.html
|   |   `-- scripts.html
|   `-- pages/
|       |-- index.html
|       |-- sobre.html
|       |-- atividades.html
|       |-- oportunidades.html
|       |-- colaboradores.html
|       `-- apoie.html
|-- templates_old/
|   |-- index.html
|   |-- sobre.html
|   |-- atividades.html
|   |-- oportunidades.html
|   |-- apoie.html
|   `-- includes/
|       |-- navbar.html
|       `-- footer.html
`-- static/
    |-- css/style.css
    |-- js/include.js
    `-- images/
        |-- atividades/
        |-- geral/
        |-- gestao/
        |-- icones/
        `-- logo/
```

## Arquivos HTML, CSS, JS e assets

HTML atual Django:

- `templates/base.html`
- `templates/includes/navbar.html`
- `templates/includes/footer.html`
- `templates/includes/scripts.html`
- `templates/pages/index.html`
- `templates/pages/sobre.html`
- `templates/pages/atividades.html`
- `templates/pages/oportunidades.html`
- `templates/pages/colaboradores.html`
- `templates/pages/apoie.html`

HTML estatico antigo:

- `templates_old/index.html`
- `templates_old/sobre.html`
- `templates_old/atividades.html`
- `templates_old/oportunidades.html`
- `templates_old/apoie.html`
- `templates_old/includes/navbar.html`
- `templates_old/includes/footer.html`

CSS e JS:

- `static/css/style.css`
- `static/js/include.js`

Assets mapeados:

- Logo: `static/images/logo/CAPICLIMA - LOGO POSITIVO VERTICAL.png`, `static/images/logo/Copy of FONTE K2D (FIGMA).png`
- Gerais: `img header principal.png`, `CAPICLIMA - HEADER 2.png`, `CAPICLIMA - APOIADORES.png`, `qrcode-pix.jpeg`, `qrCodeBackground.png`, `teste2.svg`, `teste3.svg`
- Equipe/gestao: `Gregorio.jpg`, `Augusta.jpg`, `ViniciusSanches.jpg`, `Eduarda.jpg`, `ViniciusCosta.jpeg`, `Lucas.jpeg`
- Atividades antigas/destaque: `1-coletivo-sarau-e-tempo-de-caju-cba.jpg`, `2-vs-conf-infantojuvenil-bsb.jpeg`, `3-vc-i-cupula-jovens-lideres-da-amazonia-legal.jpeg`, `4-vc-simul-ue.jpeg`
- Atividades 2024: `atividade-012024.jpeg`, `atividade-022024.jpeg`, `atividade-032024.jpeg`, `atividade-042024.jpeg`, `atividade-052024.jpeg`, `atividade-062024.png`, `atividade-072024.jpeg`
- Atividades 2025: `atividade-012025.jpeg`, `atividade-022025.jpg`, `atividade-032025.jpeg`, `atividade-042025.png`
- Iconografia: `amazonia_de_pe_iconografia_1.png`, `amazonia_de_pe_iconografia_5.png`, `amazonia_de_pe_iconografia_10.png`, `amazonia_de_pe_iconografia_11.png`, `amazonia_de_pe_iconografia_12.png`, `amazonia_de_pe_iconografia_13.png`

## Secoes e abas identificadas

### Navegacao

Original estatico:

- Inicio
- Sobre
- Atividades
- Oportunidades
- Apoie

Django atual adicionou:

- Colaboradores

Modelo proposto:

- `SiteSection` para textos curtos de navegacao, cabecalhos e chamadas.
- `SiteConfig` para logo, slogan, contatos e redes sociais.

Campos editaveis:

- Label/titulo de pagina, subtitulo, conteudo principal, ativo, ordem, imagem.
- Logo, favicon, email, telefone, WhatsApp, redes sociais, rodape.

### Inicio

Conteudo original:

- Hero com imagem `images/geral/img header principal.png`.
- Titulo: "Junte-se a nos pela justica climatica!"
- Botao "Saiba Mais".
- Secao "JUVENTUDES EM ACAO" com texto institucional.
- Tres ultimas acoes em cards.
- Secao "Nossos Parceiros" com `CAPICLIMA - APOIADORES.png`.
- Chamada visual com `CAPICLIMA - HEADER 2.png`.
- Secao de doacao.

Estado Django atual:

- Usa `DestaqueInicio` para hero.
- Usa `Atividade` com `destaque=True` para cards.
- Estatisticas e CTA ainda hard-coded.

Modelo proposto:

- `SiteSection` para hero, juventudes em acao, parceiros, CTA e apoie-home.
- `Atividade` para cards de ultimas acoes.
- `SiteConfig` para identidade e contatos globais.

Campos editaveis:

- Titulo, subtitulo/texto principal, imagem, texto do botao, URL/botao, ativo, ordem.

### Sobre

Conteudo original:

- Texto institucional sobre criacao em 24 de abril de 2024.
- Missao, formacoes, mobilizacao comunitaria, advocacy e articulacao em redes.
- Equipe com 6 membros: Gregorio Teofilo, Augusta Cesaria, Vinicius Sanches, Eduarda Almeida, Vinicius Costa e Lucas Silva.

Estado Django atual:

- Usa `ConteudoSobre` para blocos de texto.
- Usa `MembroEquipe` para equipe.
- Bio/foto/linkedin dinamicos, mas Instagram nao esta modelado.

Modelo proposto:

- `SiteSection` para texto institucional e missao.
- `MembroEquipe` para equipe/colaboradores.

Campos editaveis:

- Titulo da secao, texto rich text, imagem, icone, ativo, ordem.
- Nome, cargo, foto, bio, Instagram, LinkedIn, ordem.

### Atividades

Conteudo original:

- Filtro por ano com botoes Todos, 2025, 2024.
- Cards com imagem, titulo, tipo, data, horario, local, descricao geral, temas debatidos, resultados e galeria.
- Botao "Ver mais/Ver menos".

Atividades identificadas:

- 2025-04: Oficina "Direitos LGBTQIAPN+ e Crise Ambiental: Por uma Agenda Inclusiva na COP 30"
- 2025-03: Oficina de Formacao para a Equipe Interdisciplinar da Defensoria Publica do Estado de Mato Grosso
- 2025-02: Roda de Conversa "Juventudes Mato-Grossenses, Meio Ambiente e Justica Climatica"
- 2025-01: Instagram como Ferramenta de Educacao Popular
- 2024-07: Seminario Nacional de Juventude, Meio Ambiente e Justica Climatica
- 2024-06: Oficina "O Protagonismo da Juventude no Enfrentamento as Mudancas Climaticas"
- 2024-05: Participacao no 1o Seminario Estadual dos Objetivos do Desenvolvimento Sustentavel
- 2024-04: Sarau "E Tempo de Caju" - Virada Cultural do Movimento Amazonia de Pe
- 2024-03: Webinario "O Papel da Juventude na Construcao da Justica Climatica"
- 2024-02: Acao em Defesa das Arvores Centenarias em Chapada dos Guimaraes
- 2024-01: Roda de Conversa "Juventudes, Meio Ambiente e Justica Climatica"

Estado Django atual:

- Usa `Atividade` com `nome`, `data`, `descricao`, `imagem`, `imagem_local`, `local`, `destaque`.
- Nao possui campos separados para tipo, horario, temas/resultados/galeria.

Modelo proposto:

- Manter `Atividade` como modelo especializado, pois a pagina exige dados alem de `SiteSection`.
- Ampliar `Atividade` com tipo, horario, texto extra e ativo, ou manter rich text em descricao para os blocos longos.

Campos editaveis:

- Nome, tipo, data, horario, local, descricao rich text, imagem, imagem local fallback, destaque, ativo.

### Oportunidades

Conteudo original:

Tabela com 5 oportunidades:

- Acao de limpeza em parceria com a Asmat; descricao "A definir"; inicio outubro 2025; fim outubro 2025; link `https://forms.gle/exemplo1`.
- Oficina de reflorestamento; descricao "A definir"; inicio outubro 2025; fim outubro 2025; link `https://forms.gle/exemplo2`.
- Atividade de educacao ambiental com ensino medio; descricao "A definir"; inicio outubro 2025; fim outubro 2025; link `https://forms.gle/exemplo3`.
- COP 30 em Belem do Para; descricao "A definir"; inicio novembro 2025; fim novembro 2025; link `https://forms.gle/exemplo4`.
- Confraternizacao de fim de ano; descricao "A definir"; inicio dezembro 2025; fim dezembro 2025; link `https://forms.gle/exemplo5`.

Estado Django atual:

- Template tem 4 cards hard-coded: Educador Ambiental, Gestor de Redes Sociais, Analista de Projetos, Mobilizador Comunitario.
- Nao existe modelo `Opportunity`/`Oportunidade`.

Modelo proposto:

- `Opportunity` com titulo, descricao rich text, link, data_inicio, data_fim, ativo e ordem.
- View deve filtrar oportunidades ativas e nao expiradas.

Campos editaveis:

- Titulo, descricao, link de inscricao, data de inicio, data de fim, ativo, ordem.

### Apoie

Conteudo original:

- Card de doacao com QR Code Pix `qrcode-pix.jpeg`.
- Texto de apoio financeiro.

Estado Django atual:

- Usa `ConfiguracaoSite` para chave Pix, QR Code, email, WhatsApp, redes.
- Texto de formas de apoio ainda hard-coded.

Modelo proposto:

- `SiteConfig` para Pix, QR Code e contatos.
- `SiteSection` para textos da pagina Apoie e blocos de apoio.

Campos editaveis:

- Chave Pix, QR Code, texto da chamada, emails, WhatsApp, redes e textos dos blocos.

### Rodape

Conteudo original:

- Redes sociais Instagram/Twitter.
- Copyright 2025 CapiClima.
- Contato por email e telefone.

Estado Django atual:

- Parcialmente dinamico via `ConfiguracaoSite`.

Modelo proposto:

- `SiteConfig`.

Campos editaveis:

- Nome do site, slogan, texto de rodape, email, telefone, WhatsApp, Instagram, Twitter/X, Facebook, YouTube.

## Variaveis de cor e fontes

Variaveis CSS em `static/css/style.css`:

- `--color-primary: #0D330E`
- `--color-primary-light: #069460`
- `--color-primary-dark: #073D21`
- `--color-secondary: #E54210`
- `--color-secondary-light: #FF7A3D`
- `--color-surface: #FFFFFF`
- `--color-surface-alt: #F0F8FF`
- `--color-bg: #F0F8FF`
- `--color-text: #333333`
- `--color-text-muted: #666666`
- `--color-text-light: #FFFFFF`
- `--color-border: #DDDDDD`
- `--font-heading: 'Outfit', sans-serif`
- `--font-body: 'Inter', sans-serif`
- `--radius-sm: 5px`
- `--radius-md: 10px`
- `--radius-lg: 15px`

Cores adicionais usadas diretamente:

- Branco: `#FFF`
- Verde Bootstrap/acao: `#28a745`, hover `#218838`
- Overlay: `rgba(0, 0, 0, 0.4)`
- Bordas/texto translucidos em branco: `rgba(255,255,255,0.1-0.9)`

Observacao: ha referencias a `var(--color-accent)` em `templates/pages/oportunidades.html`, mas essa variavel nao existe no CSS atual. Deve ser corrigida para uma variavel existente sem mudar a paleta.

## Modelos Django existentes

- `DestaqueInicio`: titulo, subtitulo, imagem, ativo, ordem.
- `ConteudoSobre`: titulo_secao, texto_informativo, imagem, icone, ordem.
- `Atividade`: nome, data, descricao, imagem, imagem_local, local, destaque.
- `MembroEquipe`: nome, cargo, foto, foto_local, bio, linkedin, ordem.
- `ConfiguracaoSite`: identidade, contato, redes sociais, doacoes e rodape.

## Mapa secoes -> modelo Django proposto

| Secao/Aba | Modelo proposto | Motivo |
| --- | --- | --- |
| Navbar | `SiteConfig` + template | Links sao estruturais; logo/identidade globais ficam em config. |
| Home hero | `SiteSection` | Titulo, subtitulo, imagem e ativo sao editaveis no admin. |
| Home juventudes | `SiteSection` | Texto institucional editavel sem mexer em template. |
| Ultimas acoes | `Atividade` | Conteudo possui data, imagem e destaque. |
| Parceiros | `SiteSection` | Imagem e texto de parceiros editaveis. |
| Sobre institucional | `SiteSection` | Rich text e imagem opcionais. |
| Equipe/Colaboradores | `MembroEquipe` | Entidade repetivel com foto, cargo e bio. |
| Atividades | `Atividade` | Entidade repetivel com data, local, imagem e rich text. |
| Oportunidades | `Opportunity` | Entidade repetivel com data de inicio/fim e link. |
| Apoie | `SiteSection` + `SiteConfig` | Textos em secoes; Pix/contato em config global. |
| Footer | `SiteConfig` | Dados globais e redes sociais. |

## Decisoes de arquitetura

- Preservar a app `apps.ong`, os templates Django ja criados e o CSS atual, porque a migracao parcial ja esta funcional e o `check` passa.
- Ajustar a dependencia principal para Django 5.x, pois o AGENTS.md exige Django 5.x e o projeto hoje aponta Django 6.x.
- Introduzir `SiteSection`, `Opportunity` e `SiteConfig` para cumprir o contrato arquitetural do AGENTS.md, mantendo modelos especializados como `Atividade` e `MembroEquipe` onde a estrutura e repetivel.
- Usar CKEditor 5 ja presente no projeto para campos rich text, evitando instalar um segundo editor.
- Manter fallback para assets em `static/` para preservar o visual quando nao houver upload no admin.
- Implementar permissao por middleware/admin e grupos `Colaboradores` e `Admin`, pois o admin padrao do Django nao impede, sozinho, que um usuario `is_staff` fora dos grupos veja `/admin/`.
- Validar extensoes de imagem nos campos de upload com lista permitida: `jpg`, `jpeg`, `png`, `webp`.
- Corrigir oportunidades para CRUD no admin e renderizacao dinamica no frontend, filtrando por `ativo=True` e `data_fim >= hoje`.
- Criar seed inicial idempotente para popular config, secoes, atividades, equipe, grupos e oportunidades.
