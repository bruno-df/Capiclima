# Plano de Implementacao - CMS Django CapiClima

Data do plano: 2026-06-08

Base: `RESEARCH.md`.

## 1. Modelos Django (models.py)

### `SiteSection`

Uso: abas/secoes editaveis, blocos institucionais, headers de pagina e chamadas.

Campos:

- `nome`: titulo administrativo.
- `slug`: identificador estavel para templates.
- `titulo`: titulo exibido no site.
- `texto_principal`: rich text via CKEditor.
- `imagem`: upload opcional com validacao `jpg`, `jpeg`, `png`, `webp`.
- `botao_texto`: texto opcional de CTA.
- `botao_url`: URL opcional de CTA.
- `ordem`: ordenacao.
- `ativo`: controla exibicao.

Decisao: criar este modelo sem remover imediatamente os modelos especializados existentes. Ele cobre textos globais e evita forcar atividades/equipe em um modelo generico demais.

### `Opportunity`

Uso: oportunidades, vagas, editais, inscricoes e chamadas abertas.

Campos:

- `titulo`
- `descricao`: rich text via CKEditor.
- `link`
- `data_inicio`
- `data_fim`
- `ativo`
- `ordem`
- `criado_em`
- `atualizado_em`

Regras:

- Exibir no frontend apenas `ativo=True` e oportunidades sem expiracao ou com `data_fim >= hoje`.
- Ordenar por `data_inicio`, `data_fim`, `ordem`.

### `SiteConfig`

Uso: configuracoes globais, substituindo gradualmente `ConfiguracaoSite`.

Campos:

- Logo, favicon, slogan, nome do site.
- Email, telefone, WhatsApp, endereco.
- Instagram, Twitter/X, Facebook, YouTube.
- Chave Pix, QR Code Pix.
- Texto do rodape.

Regra:

- Singleton com `load()`, `save()` fixando `pk=1` e bloqueio de exclusao no admin.

### Modelos mantidos e ampliados

- `Atividade`: manter, pois a pagina tem estrutura propria por data/local/destaque. Adicionar `tipo`, `horario` e `ativo` se necessario para aproximar o conteudo antigo.
- `MembroEquipe`: manter. Adicionar `instagram` para preservar links do site antigo.
- `DestaqueInicio` e `ConteudoSobre`: manter como compatibilidade, mas novos textos globais devem preferir `SiteSection`.

## 2. Painel Administrativo (admin.py)

Objetivo: Django Admin como CMS dos colaboradores.

Acoes:

- Registrar `SiteSection`, `Opportunity`, `SiteConfig`, `Atividade`, `MembroEquipe`, `DestaqueInicio`, `ConteudoSobre`.
- Usar `list_display`, `search_fields`, `list_filter`, `date_hierarchy` quando houver datas.
- Usar `list_editable` somente em campos simples como `ativo`, `ordem`, `destaque`.
- Integrar rich text via `django-ckeditor-5` nos campos longos.
- Adicionar preview inline de imagens nos admins que tenham imagem/foto/logo/QR Code.
- Bloquear exclusao/criacao extra do singleton `SiteConfig`.
- Melhorar titulos do admin para linguagem de colaborador.

## 3. Sistema de Permissoes

Grupos:

- `Colaboradores`: pode acessar `/admin/` e gerenciar conteudo do site.
- `Admin`: acesso total aos modelos do projeto.

Regras:

- Usuario anonimo continua vendo a tela de login do admin.
- Usuario autenticado sem grupo `Colaboradores` ou `Admin` recebe pagina 403 customizada.
- Usuario sem `is_staff=True` nao entra no admin, mesmo que tenha grupo.
- Superusuario e grupo `Admin` sao tratados como acesso total.

Implementacao:

- Middleware `AdminGroupRequiredMiddleware` para proteger `/admin/`.
- Data migration ou comando seed para criar grupos e permissoes.
- Template `templates/403.html`.
- Testes cobrindo acesso permitido e negado.

## 4. Views e Templates

Views:

- `IndexView`: destacar hero/secoes via `SiteSection`, atividades em destaque via `Atividade`.
- `SobreView`: texto via `SiteSection`/`ConteudoSobre`, equipe via `MembroEquipe`.
- `AtividadesView`: listar apenas `ativo=True`, filtro por ano, paginacao.
- `OportunidadesView`: listar `Opportunity` ativas e nao expiradas.
- `ApoieView`: textos via `SiteSection`, dados globais via `SiteConfig`.
- `ColaboradoresView`: equipe via `MembroEquipe`.

Templates:

- Manter `base.html`, `includes/navbar.html`, `includes/footer.html` e `static/css/style.css`.
- Converter oportunidades hard-coded para loop dinamico sem redesenhar a pagina.
- Corrigir `var(--color-accent)` para variavel existente da paleta.
- Renderizar rich text com `|safe` apenas para campos editados por usuarios autenticados no admin.
- Manter fallback para imagens em `static/images/` quando nao houver upload.

Context processors:

- Atualizar para `SiteConfig.load()`.
- Manter alias de compatibilidade quando necessario.

## 5. Upload de Imagens

Configuracao:

- `MEDIA_ROOT = BASE_DIR / "media"`
- `MEDIA_URL = "/media/"`
- Em desenvolvimento, servir `MEDIA_URL` via `static()`.
- Em producao, usar storage configurado por variaveis de ambiente quando aplicavel.

Validacao:

- Extensoes permitidas: `jpg`, `jpeg`, `png`, `webp`.
- Aplicar validadores em campos de imagem/foto/logo/favicon/QR Code.
- Manter `Pillow` para validacao de imagem do Django.

Preview:

- Metodo reutilizavel no admin para exibir thumbnails pequenos com link para a imagem.

## 6. Gerenciamento de Oportunidades

CRUD:

- CRUD completo no admin via `OpportunityAdmin`.
- Filtros por `ativo`, `data_inicio`, `data_fim`.
- Busca por `titulo` e `descricao`.
- Ordenacao por `data_inicio`, `data_fim`, `ordem`.

Frontend:

- Exibir somente oportunidades ativas.
- Ocultar automaticamente oportunidades expiradas.
- Estado vazio quando nenhuma oportunidade estiver aberta.
- Link de inscricao opcional: se vazio, orientar contato por email/WhatsApp.

Seed:

- Criar oportunidades iniciais com base em `templates_old/oportunidades.html`.

## Ordem de implementacao

1. Ajustar estrutura Django para o alvo: settings, urls, app, Django 5.x e documentos de progresso.
2. Criar/ajustar modelos e migrations.
3. Customizar admin, previews e permissoes por grupos.
4. Converter oportunidades e secoes dos templates para dados dinamicos.
5. Ajustar views, URLs e context processor.
6. Configurar uploads e validacao de imagens.
7. Criar seed inicial idempotente (`seed_data.py` e/ou comando).
8. Testar fluxo de edicao, permissoes e renderizacao.
9. Atualizar README com setup local e deploy.

## Checklist de validacao por etapa

- Codigo funciona sem erros: `python manage.py check`.
- Migrations aplicam: `python manage.py migrate`.
- Permissoes testadas: colaborador acessa, usuario fora dos grupos recebe 403.
- Layout preservado: comparar paginas principais em desktop e mobile.
- Imagens carregam por upload ou fallback local.
- Rich text renderiza no frontend.

## Dependencias planejadas

- `django==5.2.15`, ultima versao 5.2.x publicada no PyPI em 2026-06-03.
- `django-ckeditor-5==0.2.20`, ultima versao publicada no PyPI em 2026-02-21.
- Manter dependencias ja usadas se necessarias para migrations historicas e upload atual.
- Evitar novos pacotes fora do necessario para cumprir o CMS.
