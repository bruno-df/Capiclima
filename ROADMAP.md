# ROADMAP.md — CapiClima: Mapeamento Técnico Completo

> **Gerado em:** 23/06/2026
> **Base de código:** Commit atual no workspace `c:\Users\bruno\Capiclima`
> **Metodologia:** Leitura completa de todos os arquivos listados na Fase 1 do `capiclima_roadmap_session.md`, sem suposições.

---

## 1. Configuração e Boot do Projeto

### Fluxo de Inicialização

```
.env (load_dotenv)
  → capiclima/settings.py (variáveis, apps, middleware, templates, banco, Cloudinary, CKEditor, Jazzmin)
    → capiclima/urls.py (rotas raiz)
      → capiclima/wsgi.py ou capiclima/asgi.py (entry point do servidor)
```

### Variáveis de Ambiente e Efeitos

| Variável               | Obrigatória | Efeito                                                                 |
|-------------------------|-------------|------------------------------------------------------------------------|
| `SECRET_KEY`           | Sim         | Se ausente, `RuntimeError` é lançado — o projeto não inicia.           |
| `DEBUG`                | Não         | Default `False`. Quando `True`, serve arquivos estáticos/media localmente. |
| `DATABASE_URL`         | Não         | Se presente, usa PostgreSQL via `dj_database_url`. Senão, SQLite local. |
| `ALLOWED_HOSTS`        | Não         | Default: `localhost,127.0.0.1,testserver`.                              |
| `CSRF_TRUSTED_ORIGINS` | Não         | Lista de origens para CSRF (deploy com HTTPS).                         |
| `CLOUDINARY_CLOUD_NAME`| Não         | Junto com `API_KEY` e `API_SECRET`, ativa Cloudinary para uploads.     |
| `CLOUDINARY_API_KEY`   | Não         | (ver acima)                                                            |
| `CLOUDINARY_API_SECRET`| Não         | (ver acima)                                                            |
| `TIME_ZONE`            | Não         | Default: `America/Cuiaba`.                                              |

### Fallbacks Automáticos

- **Banco de dados:** Sem `DATABASE_URL` → SQLite em `db.sqlite3` na raiz.
- **Uploads de mídia:** Sem as 3 variáveis Cloudinary → `FileSystemStorage` local em `media/`.
- **Storage backend:** Definido dinamicamente via `DEFAULT_FILE_STORAGE_BACKEND` e passado a `STORAGES["default"]`.

### Comando `seed_data`

```bash
python manage.py seed_data
```

**O que faz (na ordem):**
1. `_seed_config()` — Cria/carrega o `SiteConfig` (singleton, pk=1) com valores default.
2. `_seed_groups()` — Chama `sync_cms_groups()`: cria os grupos `Admin` e `Colaboradores` e sincroniza suas permissões.
3. `_seed_singletons()` — Cria/carrega `SecaoHome`, `SecaoSobre` e `SecaoApoie` (singletons).
4. `_seed_sections()` — Cria registros em `SiteSection` (7 seções) via `get_or_create(slug=...)`.
5. `_seed_equipe()` — Cria 6 membros em `MembroEquipe` via `get_or_create(nome=...)`.
6. `_seed_atividades()` — Cria 11 atividades em `Atividade` via `get_or_create(nome=...)`.
7. `_seed_oportunidades()` — Cria 5 oportunidades em `Opportunity` via `get_or_create(titulo=...)`.

**Idempotência:** Sim — todos usam `get_or_create`, portanto execuções repetidas não duplicam dados.

### Comando `popular_dados`

```bash
python manage.py popular_dados
```

**O que faz:** Similar ao `seed_data`, mas é um comando **legado** mais antigo. Popula equipe (6 membros com bios mais completas), atividades (11 atividades) e `ConfiguracaoSite.load()`. Não cria grupos, singletons nem seções.

> **Nota:** `popular_dados` importa `ConfiguracaoSite` de `models.py`, que é apenas um alias para `SiteConfig` (`ConfiguracaoSite = SiteConfig`). Funciona, mas indica código legado.

### Comando `migrate_sitesection`

```bash
python manage.py migrate_sitesection
```

**O que faz:** Migra dados do modelo genérico `SiteSection` (seções por slug) para os novos modelos dedicados `SecaoHome`, `SecaoSobre` e `SecaoApoie`. Comando de migração one-shot — após confirmar que tudo funciona, o `SiteSection` pode ser removido.

---

## 2. Django Admin — Acesso e Permissões

### URL de Acesso

```
/admin/ → admin.site.urls (Django Admin padrão, com tema Jazzmin)
```

### Fluxo de Autenticação

```
Requisição para /admin/
  → Django SessionMiddleware (verifica sessão)
    → AuthenticationMiddleware (popula request.user)
      → AdminGroupRequiredMiddleware (verifica acesso CMS)
        → Django Admin (login form ou painel)
```

### Middleware: `AdminGroupRequiredMiddleware`

**Arquivo:** `apps/ong/middleware.py`

- **Intercepta:** Todas as requisições cujo `path_info` começa com `/admin/` ou `/ckeditor5/`.
- **Condição de bloqueio:** Usuário **autenticado** mas SEM acesso CMS → renderiza `templates/403.html` com HTTP 403.
- **Condição de passagem:** Usuário não autenticado (Django Admin mostra login), ou usuário com acesso CMS.

### Lógica de Permissão: `user_has_cms_access(user)`

**Arquivo:** `apps/ong/permissions.py`

```
user.is_authenticated AND user.is_active AND user.is_staff
  → user.is_superuser? → Acesso total (True)
  → Senão: user pertence ao grupo "Admin" ou "Colaboradores"? → True
  → Senão: → False (middleware retorna 403)
```

### Comportamento por Grupo

| Grupo              | Acesso ao painel | Modelos visíveis                                            |
|--------------------|-------------------|-------------------------------------------------------------|
| **Superuser**      | Total             | Todos os modelos, incluindo auth.User                       |
| **Admin**          | Total             | Recebe TODAS as permissions do sistema                      |
| **Colaboradores**  | Restrito          | Permissões CRUD sobre: `atividade`, `conteudosobre`, `destaqueinicio`, `membroequipe`, `opportunity`, `secaoapoie`, `secaohome`, `secaosobre`, `siteconfig`, `sitesection` |
| Sem grupo (staff)  | 403               | Página de acesso negado                                     |

### Permissão customizada no `admin.site`

```python
admin.site.has_permission = lambda request: user_has_cms_access(request.user)
```

Isso substitui a verificação default do Django Admin (`is_staff`) pela lógica customizada baseada em grupos.

### Proxy Models

> ⚠️ Não encontrado no código — possível TODO. Não existem proxy models. A organização do painel é feita via `JAZZMIN_SETTINGS["order_with_respect_to"]` e ícones customizados por modelo.

### Tema do Admin: Jazzmin

- **Tema visual:** `flatly`
- **Sidebar:** `sidebar-dark-success`
- **Cores de acento:** `accent-success` (verde)
- **Modelos ocultos:** `auth.Group` (grupos são gerenciados apenas via `sync_cms_groups`)
- **Busca global:** `Atividade`, `MembroEquipe`, `Opportunity`
- **Link "Ver site":** Abre `/` em nova aba no topo do admin.

---

## 3. Django Admin — Gestão de Conteúdo

### 3.1 `Atividade` (AtividadeAdmin)

| Aspecto             | Detalhes                                                                        |
|---------------------|----------------------------------------------------------------------------------|
| **Painel**          | "Atividades"                                                                     |
| **Ícone**           | `fas fa-leaf`                                                                    |
| **list_display**    | `nome`, `tipo`, `data`, `local`, `destaque`, `ativo`                             |
| **list_editable**   | `destaque`, `ativo` (editáveis direto na listagem)                               |
| **list_filter**     | `ativo`, `destaque`, `tipo`, `data`                                              |
| **search_fields**   | `nome`, `tipo`, `local`, `descricao`, `temas_debatidos`, `resultados_encaminhamentos` |
| **date_hierarchy**  | `data`                                                                           |
| **Fieldsets**       | 4 grupos: "Informações principais", "Imagem da atividade" (com preview), "Conteúdo da atividade" (3 CKEditor), "Exibição no site" |
| **readonly_fields** | `imagem_preview` (via `ImagePreviewMixin`)                                       |
| **Imagem Cloudinary** | Upload para pasta `atividades/`, validação de extensão (`jpg, jpeg, png, webp`)  |

### 3.2 `DestaqueInicio` (DestaqueInicioAdmin)

| Aspecto             | Detalhes                                                                 |
|---------------------|---------------------------------------------------------------------------|
| **Painel**          | "Destaques de Inicio"                                                     |
| **Ícone**           | `fas fa-images`                                                           |
| **list_display**    | `titulo`, `ativo`, `ordem`, `link_botao`                                  |
| **list_editable**   | `ativo`, `ordem`                                                          |
| **list_filter**     | `ativo`                                                                   |
| **search_fields**   | `titulo`, `subtitulo`, `link_botao`                                       |
| **Fieldsets**       | 3 grupos: "Conteúdo do banner" (título, subtítulo, imagem, preview), "Botão do banner" (texto, link, abrir nova aba), "Exibição" |
| **Imagem Cloudinary** | Upload para pasta `inicio/`                                               |

### 3.3 `Parceiro` (ParceiroAdmin)

| Aspecto             | Detalhes                                                         |
|---------------------|-------------------------------------------------------------------|
| **Painel**          | "Página Inicial — Parceiros"                                      |
| **Ícone**           | `fas fa-handshake`                                                |
| **list_display**    | `nome`, `ativo`, `ordem`, `link`                                  |
| **list_editable**   | `ativo`, `ordem`                                                  |
| **list_filter**     | `ativo`                                                           |
| **search_fields**   | `nome`, `link`                                                    |
| **Imagem Cloudinary** | Upload para pasta `parceiros/`                                    |

> ⚠️ **Divergência:** O modelo `Parceiro` (`parceiro`) **não está** listado em `COLLABORATOR_MODEL_NAMES` em `permissions.py`. Isso significa que usuários do grupo "Colaboradores" **não têm permissões CRUD** para parceiros — apenas Admin/superusers podem gerenciá-los.

### 3.4 `SecaoApoie` (SecaoApoieAdmin)

| Aspecto             | Detalhes                                                         |
|---------------------|-------------------------------------------------------------------|
| **Painel**          | "Página Apoie"                                                     |
| **Ícone**           | `fas fa-heart`                                                     |
| **Comportamento**   | **Singleton** — lista redireciona para form (pk=1), sem delete, add condicional |
| **Fieldsets**       | 1 grupo: "Pix / Doação" com campos `pix`, `qrcode_pix`, `imagem_preview` |
| **Imagem Cloudinary** | Upload para pasta `apoie/` (QR Code)                              |

### 3.5 `Opportunity` (OpportunityAdmin)

| Aspecto             | Detalhes                                                                        |
|---------------------|----------------------------------------------------------------------------------|
| **Painel**          | "Oportunidades — Planilha de Inscrições"                                         |
| **Ícone**           | `fas fa-table`                                                                   |
| **list_display**    | `titulo`, `tipo`, `data_fim`, `ativo`, `ordem`, `esta_aberta` (property calculada) |
| **list_editable**   | `tipo`, `data_fim`, `ativo`, `ordem`                                             |
| **list_filter**     | `ativo`, `tipo`, `data_fim`                                                      |
| **search_fields**   | `titulo`, `tipo`, `descricao`, `link`                                            |
| **date_hierarchy**  | `data_fim`                                                                       |
| **Fieldsets**       | 3 grupos: "Dados da oportunidade", "Inscrição" (link + datas), "Exibição no site" |
| **Sem imagem**      | Este modelo não possui campos de imagem.                                         |
| **Coluna `esta_aberta`** | Property calculada: `ativo AND (data_fim is None OR data_fim >= hoje)`. Exibida como coluna read-only na listagem. |

### 3.6 `MembroEquipe` (MembroEquipeAdmin)

| Aspecto             | Detalhes                                                         |
|---------------------|-------------------------------------------------------------------|
| **Painel**          | "Membros da Equipe"                                               |
| **Ícone**           | `fas fa-users`                                                    |
| **list_display**    | `nome`, `cargo`, `ordem`                                          |
| **list_editable**   | `ordem`                                                           |
| **search_fields**   | `nome`, `cargo`, `bio`                                            |
| **Fieldsets**       | 3 grupos: "Dados pessoais" (nome, cargo, foto, foto_local, preview, bio), "Links" (instagram, linkedin — colapsável), "Exibição" (ordem) |
| **Imagem Cloudinary** | Upload para pasta `equipe/`                                       |
| **Fallback imagem** | `foto` (Cloudinary) → `foto_local` (caminho estático local)       |

### 3.7 `SiteConfig` (SiteConfigAdmin)

| Aspecto             | Detalhes                                                         |
|---------------------|-------------------------------------------------------------------|
| **Painel**          | "Configuracao do Site"                                             |
| **Ícone**           | `fas fa-cog`                                                      |
| **Comportamento**   | **Singleton** — lista redireciona para form (pk=1), sem delete     |
| **readonly_fields** | `imagem_preview`, `logo_preview`                                  |
| **Fieldsets**       | 3 grupos: "Identidade do site" (nome, slogan, logo + preview, favicon), "Contato" (email, telefone, whatsapp, endereço), "Redes sociais" (instagram, twitter, facebook, youtube) |
| **Imagem Cloudinary** | Logo e favicon → pasta `config/`                                  |

### 3.8 Modelos NÃO registrados no Admin

| Modelo        | Status no Admin                                                       |
|---------------|-----------------------------------------------------------------------|
| `SecaoHome`   | ⚠️ **Não registrado.** Não aparece no painel. Editável apenas via shell/seed. |
| `SecaoSobre`  | ⚠️ **Não registrado.** Não aparece no painel. Editável apenas via shell/seed. |
| `SiteSection` | ⚠️ **Não registrado.** Modelo legado mantido por compatibilidade.      |
| `ConteudoSobre` | ⚠️ **Não registrado.** Não pode ser gerenciado pelo painel.            |

### Validação de Imagem

```python
image_extension_validator(value)
```

- Aceita: `jpg`, `jpeg`, `png`, `webp`
- Rejeita com `ValidationError` qualquer outra extensão.
- Aplicada como validator em todos os `CloudinaryField` do projeto.

### `ImagePreviewMixin`

Mixin reutilizável que adiciona `imagem_preview` como campo read-only. Procura automaticamente pelos campos `imagem`, `imagem_banner`, `foto`, `logo`, `qrcode_pix`, `favicon` (nessa ordem) e renderiza um `<img>` com link clicável.

### `SingletonAdminMixin`

- `has_add_permission`: Retorna `False` se o registro já existe (impede duplicação).
- `has_delete_permission`: Sempre `False`.
- `changelist_view`: Redireciona direto para o form de edição (pk do registro existente).

---

## 4. Página Inicial (`/`)

### Rota e View

```
GET / → ong:index → IndexView (TemplateView) → templates/pages/index.html
```

### Dados do Contexto

| Variável                | Fonte                                                       | Tipo         |
|-------------------------|-------------------------------------------------------------|--------------|
| `title`                | Hardcoded `"Inicio"`                                         | `str`        |
| `destaques`            | `DestaqueInicio.objects.filter(ativo=True).order_by("ordem", "id")` | `QuerySet`   |
| `atividades_destaque`  | `Atividade.objects.filter(destaque=True, ativo=True)[:3]`    | `QuerySet`   |
| `total_atividades`     | `Atividade.objects.filter(ativo=True).count()`               | `int`        |
| `total_equipe`         | `MembroEquipe.objects.count()`                               | `int`        |
| `parceiros`            | `Parceiro.objects.filter(ativo=True).order_by("ordem", "nome")` | `QuerySet`   |
| `config_site`          | Via `context_processors.configuracao_site` (global)          | `SiteConfig` |

### Estrutura da Página

```
┌─────────────────────────────────────────────┐
│ HERO — Carrossel de DestaqueInicio          │
│   Cada slide: imagem (Cloudinary/fallback)  │
│   + título + subtítulo + botão opcional     │
│   Se nenhum destaque: hero estático default │
├─────────────────────────────────────────────┤
│ JUVENTUDES EM AÇÃO                          │
│   Título/texto de secao_home (ver nota)     │
├─────────────────────────────────────────────┤
│ SVG de transição (teste2.svg)               │
├─────────────────────────────────────────────┤
│ NOSSAS AÇÕES (fundo laranja)                │
│   Grid de até 3 cards de atividades_destaque│
│   + Botão "Saiba mais" → /atividades/       │
├─────────────────────────────────────────────┤
│ PARCEIROS                                   │
│   Grid de logos clicáveis (ou nome-texto)   │
├─────────────────────────────────────────────┤
│ SVG de transição (teste3.svg)               │
├─────────────────────────────────────────────┤
│ STATS — Contadores animados                 │
│   Atividades | Equipe | 2024 | ∞ | 🌱       │
│   data-stats-url → /api/stats/ (polling JS) │
├─────────────────────────────────────────────┤
│ CTA — Chamada para ação                     │
│   Texto de secao_home (ver nota)            │
│   + Botões: Voluntário → /oportunidades/    │
│             Apoie → /apoie/                 │
└─────────────────────────────────────────────┘
```

> ⚠️ **Divergência detectada:** O template `index.html` referencia `{{ secao_home.titulo_juventudes }}`, `{{ secao_home.texto_juventudes }}`, `{{ secao_home.titulo_cta }}` e `{{ secao_home.texto_cta }}`. Porém, a `IndexView` **não injeta `secao_home`** no contexto, e o `context_processors.configuracao_site` injeta apenas `config_site` (SiteConfig). O `secao_home` chega como `None`/indefinido e os templates exibem apenas os valores `|default:`.

### Lógica de Destaque de Atividades

- O campo `destaque` (BooleanField) marca atividades para exibição na home.
- A query filtra `destaque=True, ativo=True` e limita a 3 resultados (sem ordering explícito além do default do model: `-data`).
- Editável na listagem do admin via `list_editable`.

### API de Contadores (`/api/stats/`)

```
GET /api/stats/ → StatsAPIView → JSON
```

Retorno:
```json
{
  "total_atividades": "<int>",
  "total_equipe": "<int>"
}
```

> ⚠️ **Divergência:** O JavaScript `stats.js` procura por `data.total_colaboradores` (linha 63), mas a API retorna `total_equipe`. Isso significa que o contador de "Equipe"/"Colaboradores" **não é atualizado em tempo real** pelo polling — apenas a animação inicial (baseada em `data-target`) funciona.

---

## 5. Página Sobre (`/sobre/`)

### Rota e View

```
GET /sobre/ → ong:sobre → SobreView (TemplateView) → templates/pages/sobre.html
```

### Dados do Contexto

| Variável              | Fonte                                               |
|------------------------|------------------------------------------------------|
| `title`               | Hardcoded `"Sobre"`                                   |
| `secao_sobre`         | `SecaoSobre.load()` (singleton)                       |
| `conteudos`           | `ConteudoSobre.objects.all()` (ordenado por `ordem`)  |
| `equipe`              | `MembroEquipe.objects.all()` (ordenado por `ordem`)   |
| `total_atividades`    | `Atividade.objects.filter(ativo=True).count()`        |
| `total_equipe`        | `MembroEquipe.objects.count()`                        |

### Estrutura da Página

```
┌─────────────────────────────────────────────┐
│ PAGE HEADER                                 │
│   secao_sobre.titulo | default              │
│   "Sobre o CapiClima"                       │
├─────────────────────────────────────────────┤
│ CONTEÚDO PRINCIPAL (se texto_principal)     │
│   Imagem institucional                      │
│   Rich text principal                       │
│   Missão (se preenchido)                    │
│   Visão (se preenchido)                     │
│   Valores (se preenchido)                   │
├─────────────────────────────────────────────┤
│ CONTEÚDOS DINÂMICOS (ConteudoSobre loop)    │
│   Para cada: ícone FA + título + imagem     │
│   + rich text                               │
├─────────────────────────────────────────────┤
│ FALLBACK (se nenhum conteúdo acima)         │
│   "Quem Somos?" + "Nossa Missão" hardcoded  │
├─────────────────────────────────────────────┤
│ STATS (igual à home)                        │
├─────────────────────────────────────────────┤
│ EQUIPE (cards compactos com foto/nome/cargo)│
│   Fallback de imagem: foto → foto_local     │
│   → ícone                                   │
│   Links sociais: Instagram, LinkedIn        │
├─────────────────────────────────────────────┤
│ CTA → link para /oportunidades/             │
└─────────────────────────────────────────────┘
```

### Renderização de Ícones Font Awesome

O campo `icone` de `ConteudoSobre` armazena a classe CSS completa do ícone (ex: `fas fa-leaf`). O template renderiza:

```html
<i class="{{ conteudo.icone }} me-2" style="color:var(--color-primary-light);"></i>
```

---

## 6. Página Equipe (`/equipe/`)

### Rota e View

```
GET /equipe/ → ong:equipe → EquipeView (TemplateView) → templates/pages/equipe.html
```

### Dados do Contexto

| Variável | Fonte                                          |
|----------|-------------------------------------------------|
| `title`  | Hardcoded `"Equipe"`                             |
| `equipe` | `MembroEquipe.objects.all()` (ordenado por `ordem` via Meta) |

### Estrutura da Página

- **Page header** com título e subtítulo fixos.
- **Loop de membros** renderizados como `colaborador-card` (layout horizontal):
  - **Imagem:** Cascata de fallback:
    1. `membro.foto` (Cloudinary) → aplica `cloudinary_optimized` filter
    2. `membro.foto_local` (caminho estático)
    3. Ícone placeholder `fas fa-user`
  - **Conteúdo:** Nome (h3) + ícones sociais inline (Instagram, LinkedIn) + cargo (h5) + bio (parágrafo)
- **Empty state:** "Equipe em construção" se nenhum membro cadastrado.

### Ordenação

Definida no `Meta` do modelo: `ordering = ["ordem"]`. Os membros aparecem na ordem definida pelo campo `ordem` (editável no admin via `list_editable`).

---

## 7. Página Atividades (`/atividades/`)

### Rota e View

```
GET /atividades/ → ong:atividades → AtividadesView (ListView) → templates/pages/atividades.html
```

### Dados do Contexto

| Variável           | Fonte                                                                |
|--------------------|-----------------------------------------------------------------------|
| `atividades`       | `Atividade.objects.filter(ativo=True)`, opcionalmente filtrado por `?ano=YYYY` |
| `anos`             | `Atividade.objects.filter(ativo=True).dates("data", "year", order="DESC")` |
| `ano_selecionado`  | `request.GET.get("ano", "")`                                         |
| `title`            | Hardcoded `"Atividades"`                                              |

### Funcionalidades

- **Paginação:** `paginate_by = 9` (9 atividades por página).
- **Filtro por ano:** Query param `?ano=2024` filtra por `data__year`.
- **Barra de filtros:** Botões para cada ano + botão "Todas".

### Estrutura de Cada Card de Atividade

```
┌─────────────────────────────────────────────┐
│ HEADER — ícone folha + nome da atividade     │
├─────────────────────────────────────────────┤
│ RESUMO COMPACTO                             │
│   [thumbnail]  Tipo | Data | Horário | Local │
│                [Botão "Ver mais"]            │
├─────────────────────────────────────────────┤
│ EXPANDIDO (collapse Bootstrap)              │
│   Imagem grande                             │
│   Descrição (rich text)                     │
│   Temas Debatidos (rich text, se preenchido)│
│   Resultados e Encaminhamentos (rich text)  │
└─────────────────────────────────────────────┘
```

### Fallback de Imagem

1. `atividade.imagem` (Cloudinary) → aplica `cloudinary_optimized`
2. `atividade.imagem_local` (caminho estático)
3. Placeholder div com ícone `fas fa-image`

### Comportamento de "Ver mais"

- Usa Bootstrap `collapse` com `data-bs-toggle`.
- O botão alterna a visibilidade da div `#atividade-extra-{{ atividade.id }}`.
- O conteúdo expandido mostra: imagem em tamanho grande + `descricao` + `temas_debatidos` + `resultados_encaminhamentos`.

### Campos Rich Text (CKEditor 5)

- `descricao` — Descrição principal (sempre presente).
- `temas_debatidos` — Exibido apenas se preenchido, dentro do "Ver mais".
- `resultados_encaminhamentos` — Exibido apenas se preenchido, dentro do "Ver mais".

### Ordenação

Default do model: `ordering = ["-data"]` (mais recente primeiro).

---

## 8. Página Oportunidades (`/oportunidades/`)

### Rota e View

```
GET /oportunidades/ → ong:oportunidades → OportunidadesView (TemplateView) → templates/pages/oportunidades.html
```

### Dados do Contexto

| Variável          | Fonte                                                        |
|-------------------|--------------------------------------------------------------|
| `title`           | Hardcoded `"Oportunidades"`                                   |
| `oportunidades`   | `Opportunity.abertas().order_by("ordem", "data_inicio")`     |

### Lógica de Filtragem: `Opportunity.abertas()`

```python
@classmethod
def abertas(cls):
    hoje = timezone.localdate()
    return cls.objects.filter(ativo=True).filter(
        Q(data_fim__isnull=True) | Q(data_fim__gte=hoje)
    )
```

**Significado:** Retorna oportunidades que:
1. Estão ativas (`ativo=True`), **E**
2. Não têm data de fim (`data_fim` é nulo → permanente), **OU** têm data de fim no futuro/hoje.

### Property `esta_aberta`

```python
@property
def esta_aberta(self):
    hoje = timezone.localdate()
    return self.ativo and (self.data_fim is None or self.data_fim >= hoje)
```

**Uso no Admin:** Aparece como coluna read-only na listagem (`list_display`). Mostra `True`/`False` para cada oportunidade.

**Uso no template público:** Não é utilizada diretamente no template `oportunidades.html` — o template confia na query `abertas()` para filtrar, então todas as oportunidades exibidas já estão abertas.

### Estrutura da Página

- **Tabela responsiva** com colunas:
  - Oportunidade (título em negrito)
  - Tipo (badge verde ou "Não informado")
  - Descrição (truncada a 28 palavras)
  - Término de inscrição (data formatada ou "Sem prazo definido")
  - Link de inscrição (botão "Inscrever-se" abrindo em nova aba, ou "Indisponível")
- **Empty state:** "Sem oportunidades no momento" se nenhuma aberta.

---

## 9. Página Apoie (`/apoie/`)

### Rota e View

```
GET /apoie/ → ong:apoie → ApoieView (TemplateView) → templates/pages/apoie.html
```

### Dados do Contexto

| Variável       | Fonte                             |
|----------------|-----------------------------------|
| `title`        | Hardcoded `"Apoie"`                |
| `secao_apoie`  | `SecaoApoie.load()` (singleton)   |
| `config_site`  | Via context_processor (global)    |

### Estrutura da Página

```
┌─────────────────────────────────────────────┐
│ PAGE HEADER                                 │
├─────────────────────────────────────────────┤
│ FORMAS DE APOIO                             │
│                                             │
│  Voluntariado                               │
│   Texto hardcoded + botão → /oportunidades/ │
│                                             │
│  Doação Financeira                          │
│   Texto hardcoded                           │
│   Pix Box:                                  │
│     Se secao_apoie.pix → exibe chave        │
│     Se secao_apoie.qrcode_pix → exibe QR    │
│     Senão → fallback coletivocapiclima@gmail│
│                                             │
│  Parcerias Empresariais                     │
│   Texto hardcoded                           │
│                                             │
│  Compartilhe                                │
│   Botões redes sociais de config_site       │
├─────────────────────────────────────────────┤
│ CTA Final                                   │
│   E-mail + WhatsApp (de config_site)        │
└─────────────────────────────────────────────┘
```

### Por que apenas Pix é dinâmico?

O modelo `SecaoApoie` contém **apenas** `pix` (CharField) e `qrcode_pix` (CloudinaryField). Os demais textos da página (voluntariado, parcerias, compartilhe) são **hardcoded no template**. Isso é uma decisão de design: o conteúdo de apoio raramente muda, exceto a chave Pix e o QR Code, que são os únicos campos editáveis pelo admin.

> ⚠️ **Divergência:** O `migrate_sitesection` referencia campos como `texto_voluntariado`, `texto_doacao`, `texto_parcerias`, `texto_compartilhe` no `SecaoApoie`, mas esses campos **não existem** no modelo atual. Isso indica que o comando de migração está desatualizado em relação ao modelo — foi criado antes da simplificação do `SecaoApoie`.

---

## 10. Navbar, Footer e Componentes Globais

### Context Processor: `configuracao_site`

**Arquivo:** `apps/ong/context_processors.py`

```python
def configuracao_site(request):
    config = SiteConfig.load()  # singleton pk=1
    return {"config_site": config}
```

- Registrado em `settings.TEMPLATES[0]["OPTIONS"]["context_processors"]`.
- **Injeta `config_site`** em TODOS os templates do projeto.
- **Tratamento de erro:** Se `SiteConfig.load()` falhar, retorna `config_site = None`.

### `base.html` — Template Base

```
<html>
<head>
  Favicon (config_site.favicon)
  Google Fonts: Inter + Outfit
  Bootstrap 5.3 CSS (CDN)
  Font Awesome 6 (CDN)
  static/css/style.css
  {% block extra_css %}
  <title>{% block title %}</title>
</head>
<body>
  {% include "includes/navbar.html" %}
  <main>{% block content %}</main>
  {% include "includes/footer.html" %}
  {% include "includes/scripts.html" %}
  {% block extra_js %}
</body>
</html>
```

### `navbar.html`

- **Posição:** `fixed-top` com classe `navbar-cap`.
- **Logo:** `config_site.logo.url` → fallback para imagem estática `images/logo/CAPICLIMA - LOGO POSITIVO VERTICAL.png`.
- **Links:** Início, Sobre, Atividades, Oportunidades, Equipe + botão especial "Apoie" (`btn-apoie`).
- **Ativo:** Link atual recebe classe `active` via `request.resolver_match.url_name`.
- **Mobile:** Collapse Bootstrap com botão hamburger.

### `footer.html`

- **3 colunas:**
  1. **Sobre:** Nome do site + slogan + ícones de redes sociais (Instagram, Twitter/X, Facebook, YouTube) — condicionais.
  2. **Links Rápidos:** Links para todas as 6 páginas.
  3. **Contato:** Email (clicável), Telefone, WhatsApp (clicável para `wa.me/`).
- **Barra inferior:** © Ano atual + nome do site.
- **Todos os dados** vêm de `config_site` com `|default:` para fallbacks textuais.

### `scripts.html`

- Bootstrap 5.3 Bundle JS (CDN, inclui Popper.js)
- `static/js/include.js` — fecha navbar mobile ao clicar em link.
- `static/js/stats.js` — animação de contadores + polling de `/api/stats/` a cada 30s.

### `403.html`

- Estende `base.html`.
- Exibe "Acesso negado" + botão "Voltar ao site" → `/`.

---

## 11. Uploads e Imagens (Cloudinary)

### Fluxo Completo de Upload

```
1. Admin → Formulário com CloudinaryField
   → Validação: image_extension_validator (jpg, jpeg, png, webp)
     → Se inválido: ValidationError

2. Upload → Cloudinary API
   → cloudinary.config(cloud_name, api_key, api_secret, secure=True)
   → Pasta definida pelo parâmetro folder= de cada campo:
       atividades/ | inicio/ | parceiros/ | sobre/
       equipe/ | config/ | apoie/ | home/

3. Cloudinary retorna → URL pública (https://res.cloudinary.com/...)
   → Salva no campo do modelo (referência Cloudinary)

4. Template → Renderização
   → Acesso: objeto.campo.url → URL completa do Cloudinary
   → Otimização via templatetag (se usado)
```

### `cloudinary_utils.py` — Template Tag

**Arquivo:** `apps/ong/templatetags/cloudinary_utils.py`

```python
@register.filter
def cloudinary_optimized(image, width=900)
```

**O que faz:**
1. Obtém a URL do campo (`.url`).
2. Se a URL contém `/upload/`, insere transformações Cloudinary: `f_auto,q_auto,w_900`.
3. Resultado: URL tipo `https://res.cloudinary.com/.../upload/f_auto,q_auto,w_900/v.../pasta/arquivo.jpg`.

**Transformações:**
- `f_auto` — Formato automático (WebP quando suportado pelo navegador).
- `q_auto` — Qualidade automática (otimização de tamanho pelo Cloudinary).
- `w_900` — Largura de 900px (redimensionamento server-side).

**Onde é usado:** `index.html` (destaques, parceiros), `equipe.html`, `atividades.html`, `apoie.html` (QR Code).

### Validação de Extensão

```python
ALLOWED_IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]

def image_extension_validator(value):
    # Extrai extensão do nome do arquivo
    # Se não está em ALLOWED_IMAGE_EXTENSIONS → ValidationError
```

Aplicada como `validators=[image_extension_validator]` em todos os `CloudinaryField` do projeto.

### Fallback para Storage Local

**Em `settings.py`:**

```python
CLOUDINARY_CONFIGURED = all([
    CLOUDINARY_CLOUD_NAME,
    CLOUDINARY_API_KEY,
    CLOUDINARY_API_SECRET
])

DEFAULT_FILE_STORAGE_BACKEND = (
    "cloudinary_storage.storage.MediaCloudinaryStorage"
    if CLOUDINARY_CONFIGURED
    else "django.core.files.storage.FileSystemStorage"
)
```

- **Com Cloudinary configurado:** Uploads vão para Cloudinary API.
- **Sem Cloudinary:** Uploads vão para `media/` local (servido em dev por `static(settings.MEDIA_URL, ...)`).

### Fallback de Imagens nos Templates

Além do fallback de storage, os templates implementam fallbacks em nível de campo:

| Modelo       | Prioridade 1         | Prioridade 2              | Prioridade 3         |
|-------------|----------------------|---------------------------|----------------------|
| Atividade   | `imagem` (Cloudinary)| `imagem_local` (static)   | Placeholder ícone    |
| MembroEquipe| `foto` (Cloudinary)  | `foto_local` (static)     | Placeholder ícone    |
| DestaqueInicio | `imagem` (Cloudinary) | Imagem estática default | —                    |
| Parceiro    | `imagem` (Cloudinary)| Nome em texto             | —                    |

---

## Resumo de Divergências Encontradas

| #  | Descrição                                                                                  | Impacto                                   |
|----|--------------------------------------------------------------------------------------------|-------------------------------------------|
| 1  | `IndexView` não injeta `secao_home` no contexto, mas o template `index.html` o referencia.  | Seções Juventudes e CTA exibem apenas valores default. |
| 2  | `StatsAPIView` retorna `total_equipe`, mas `stats.js` espera `total_colaboradores`.         | Polling a cada 30s não atualiza o contador de equipe/colaboradores. |
| 3  | `SecaoHome` e `SecaoSobre` não estão registrados no admin.                                  | Não podem ser editados pelo painel. Apenas via shell/seed. |
| 4  | `ConteudoSobre` não está registrado no admin.                                               | Não pode ser gerenciado pelo painel.       |
| 5  | `SiteSection` não está registrado no admin.                                                  | Modelo legado invisível no painel.         |
| 6  | `Parceiro` não está em `COLLABORATOR_MODEL_NAMES`.                                           | Colaboradores não têm CRUD de parceiros.   |
| 7  | `migrate_sitesection` referencia campos inexistentes no `SecaoApoie` atual.                  | Comando de migração está desatualizado.    |
| 8  | Template `sobre.html` usa `total_colaboradores` no stats, mas a view envia `total_equipe`.   | Mesmo problema do item 2 no template.     |

---

## Critérios de Aceitação — Status

- [x] Todos os 11 fluxos listados estão cobertos
- [x] O sistema de permissões (Admin / Colaboradores / sem grupo) está documentado com base no código real
- [x] O padrão Singleton (`SingletonMixin`) e seus models estão explicados
- [x] O fluxo de imagens Cloudinary (upload → armazenamento → renderização → fallback) está descrito
- [x] A lógica de filtragem de `Opportunity.abertas()` e a property `esta_aberta` estão documentadas
- [x] Nenhuma seção contém suposições não verificadas — divergências estão explicitamente marcadas
- [x] O documento está em Markdown válido e salvo como `ROADMAP.md`
