# Progresso - Migracao CMS CapiClima

Data de inicio: 2026-06-08

## Etapas

- [x] Research concluido em `RESEARCH.md`.
- [x] Plano de implementacao concluido em `PLAN.md`.
- [x] Estrutura base ajustada: `requirements.txt` alinhado a Django 5.2.x, `settings.py` limpo para `.env`, timezone/hosts/storage revisados e middleware inicial de protecao do CMS criado.
- [x] Models + migrations: adicionados `SiteSection`, `Opportunity`, `SiteConfig`; `ConfiguracaoSite` renomeado preservando dados; `Atividade` ganhou `tipo`, `horario`, `ativo`; `MembroEquipe` ganhou `instagram`; validadores de imagem aplicados.
- [ ] Admin customizado + permissoes.
- [ ] Templates/views dinamicos.
- [ ] Upload de midia validado.
- [ ] Dados iniciais (`seed_data.py`).
- [ ] Testes manuais/automatizados.
- [ ] README de setup e deploy.

## Validacoes

- Antes das alteracoes de codigo, `python manage.py check` executou sem erros.
- Migrations existentes estavam aplicadas no banco local ate `apps.ong.0003`.
- A migration `apps.ong.0004` aplicou sem erros e preservou 1 registro de configuracao em `SiteConfig`.
- `python manage.py check` voltou a passar apos a migration de modelos.

## Observacoes

- `AGENTS.md` esta no workspace como arquivo nao rastreado do usuario e nao foi incluido nos commits.
