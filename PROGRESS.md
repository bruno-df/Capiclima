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
- [ ] Testes manuais/automatizados.

## Validacoes

- Antes das alteracoes de codigo, `python manage.py check` executou sem erros.
- Migrations existentes estavam aplicadas no banco local ate `apps.ong.0003`.
- A migration `apps.ong.0004` aplicou sem erros e preservou 1 registro de configuracao em `SiteConfig`.
- `python manage.py check` voltou a passar apos a migration de modelos.
- `python manage.py check` passou sem erros apos conversao de templates e views (Bloco 4).
- `python manage.py seed_data` executou com sucesso: 7 secoes criadas, 5 oportunidades criadas, equipe e atividades preservadas.

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
