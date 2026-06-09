# Progresso - Migracao CMS CapiClima

Data de inicio: 2026-06-08

## Etapas

- [x] Research concluido em `RESEARCH.md`.
- [x] Plano de implementacao concluido em `PLAN.md`.
- [x] Estrutura base ajustada: `requirements.txt` alinhado a Django 5.2.x, `settings.py` limpo para `.env`, timezone/hosts/storage revisados e middleware inicial de protecao do CMS criado.
- [x] Models + migrations: adicionados `SiteSection`, `Opportunity`, `SiteConfig`; `ConfiguracaoSite` renomeado preservando dados; `Atividade` ganhou `tipo`, `horario`, `ativo`; `MembroEquipe` ganhou `instagram`; validadores de imagem aplicados.
- [x] Admin customizado + permissoes: admin.py com previews de imagem inline, fieldsets, singleton protegido; `permissions.py` com `sync_cms_groups`; middleware `AdminGroupRequiredMiddleware` atualizado; template `403.html`.
- [x] Templates/views dinamicos: views atualizadas para injetar `SiteSection`, `Opportunity.abertas()`, filtro `ativo=True` em atividades; oportunidades convertidas de hard-coded para loop dinamico; index usa secoes editaveis (juventudes, parceiros, CTA); sobre e colaboradores exibem Instagram dos membros; `var(--color-accent)` corrigido para `var(--color-primary-light)`; context processor atualizado para `SiteConfig`.
- [x] Dados iniciais (`seed_data.py`): comando idempotente cria SiteConfig, grupos (Colaboradores, Admin), 7 SiteSections, 6 membros, 11 atividades e 5 oportunidades.
- [x] README de setup e deploy: `README.md` com instrucoes completas e `.env.example`.
- [x] FIXES.md — Problema 1: Bugs de conteudo dinamico corrigidos.
- [x] FIXES.md — Problema 2: Admin reestruturado com modelos dedicados.
- [x] FIXES.md — Problema 3: UX do admin melhorada.
- [ ] Testes manuais/automatizados.

## FIXES.md — Detalhes das correcoes (2026-06-09)

### Problema 1 — Bugs de conteudo dinamico

| Secao | Causa raiz | Correcao |
|-------|-----------|----------|
| Apoie (voluntariado, doacao, parcerias, compartilhe) | Template `apoie.html` tinha textos hard-coded e ignorava as variaveis `secao_voluntariado`, `secao_doacao`, etc. injetadas pela view. Os dados existiam no banco (SiteSection), mas nao eram consumidos pelo template. | Template reescrito para usar `secao_apoie` (novo singleton `SecaoApoie`) com `|safe` nos campos rich text e fallbacks para texto padrao. |
| Home (juventudes, parceiros, CTA) | Funcionava mas dependia de slugs frageis no `SiteSection`. | Migrado para `SecaoHome` (singleton) com campos dedicados por secao. Template atualizado. |

### Problema 2 — Reestruturar admin com modelos dedicados

Novos modelos criados (singletons):
- `SecaoHome` — campos: titulo_principal, subtitulo, imagem_banner, titulo/texto/imagem para juventudes, parceiros, CTA.
- `SecaoSobre` — campos: titulo, texto_principal, imagem, missao, visao, valores.
- `SecaoApoie` — campos: texto/link para voluntariado, doacao, parcerias, compartilhe.
- `SingletonMixin` — mixin reutilizavel com `pk=1`, `load()` e bloqueio de delete.

Admin reestruturado:
- `SingletonAdminMixin` — redireciona listagem para formulario de edicao, bloqueia adicao/exclusao.
- Menu agrupado: Pagina Inicial, Atividades, Destaques | Pagina Apoie, Oportunidades | Pagina Sobre, Conteudos Sobre | Config do Site, Membros.
- Preview de imagens em todos os admins com imagem.

Migration de dados:
- Comando `migrate_sitesection` criado e executado — migra dados de `SiteSection` (slugs) para os novos modelos dedicados.
- `SiteSection` mantido temporariamente por compatibilidade.

Arquivos alterados:
- `apps/ong/models.py` — adicionados `SingletonMixin`, `SecaoHome`, `SecaoSobre`, `SecaoApoie`; `SiteConfig` refatorado para usar `SingletonMixin`; `help_text` adicionado.
- `apps/ong/admin.py` — reescrito com agrupamento, `SingletonAdminMixin`, `ImagePreviewMixin`.
- `apps/ong/views.py` — reescrito para usar `SecaoHome.load()`, `SecaoSobre.load()`, `SecaoApoie.load()`.
- `apps/ong/permissions.py` — adicionados `secaoapoie`, `secaohome`, `secaosobre` ao grupo Colaboradores.
- `apps/ong/apps.py` — adicionado `verbose_name = 'Gerenciamento do Site'`.
- `templates/pages/index.html` — usa `secao_home` singleton.
- `templates/pages/apoie.html` — usa `secao_apoie` singleton com `|safe`.
- `templates/pages/sobre.html` — usa `secao_sobre` singleton + `conteudos`.
- `apps/ong/management/commands/migrate_sitesection.py` — novo comando de migracao.
- `apps/ong/management/commands/seed_data.py` — atualizado para criar singletons.
- Migration `0005_secaoapoie_secaohome_secaosobre_and_more.py` criada e aplicada.

### Problema 3 — UX geral do admin

- `admin.site.site_header` = "Capiclima -- Painel de Gestao"
- `admin.site.site_title` = "Capiclima CMS"
- `admin.site.index_title` = "Bem-vindo ao painel"
- `list_display`, `list_filter`, `search_fields` mantidos/melhorados em todos os admins.
- `help_text` adicionado em campos menos obvios: logo, favicon, chave_pix, qrcode_pix, whatsapp, imagem_banner, etc.
- Ordenacao padrao definida no Meta de cada modelo (ja existia).
- `verbose_name` no AppConfig para label claro no menu.

## Validacoes

- Antes das alteracoes de codigo, `python manage.py check` executou sem erros.
- Migrations existentes estavam aplicadas no banco local ate `apps.ong.0003`.
- A migration `apps.ong.0004` aplicou sem erros e preservou 1 registro de configuracao em `SiteConfig`.
- `python manage.py check` voltou a passar apos a migration de modelos.
- `python manage.py check` passou sem erros apos conversao de templates e views (Bloco 4).
- `python manage.py seed_data` executou com sucesso: 7 secoes criadas, 5 oportunidades criadas, equipe e atividades preservadas.
- Migration `apps.ong.0005` aplicou sem erros (3 novos modelos + alteracoes SiteConfig).
- `migrate_sitesection` executou com sucesso: 3 secoes home + 4 secoes apoie migradas.
- `python manage.py check` passou sem erros apos FIXES.md.
- `seed_data` executou com sucesso: singletons criados, 44 permissoes para Colaboradores.

## Commits realizados

1. `d7d6e02` — Adiciona pesquisa da migracao CMS
2. `18595a6` — Adiciona plano de implementacao do CMS
3. `18a6f13` — Ajusta base Django 5 e protecao inicial do CMS
4. `3c7a525` — Adiciona modelos dinamicos do CMS
5. `922e272` — Customiza admin com previews de imagem, permissoes por grupo e middleware de protecao
6. `eba587b` — Converte templates e views para dados dinamicos do CMS
7. `4a2d79a` — Adiciona comando seed_data com secoes, oportunidades, grupos e dados iniciais
8. `287ab71` — Adiciona README com instrucoes de setup e .env.example

## Observacoes

- `AGENTS.md` esta no workspace como arquivo nao rastreado do usuario e nao foi incluido nos commits.
- O upload de midia ja esta configurado via Cloudinary (producao) e FileSystemStorage (desenvolvimento) com validadores de extensao nos models. Nenhum bloco adicional necessario.
- `SiteSection` mantido temporariamente por compatibilidade com migrations e dados existentes. Pode ser removido em versao futura apos validacao completa.
