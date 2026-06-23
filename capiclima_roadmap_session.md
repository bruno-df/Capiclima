# SESSION DOC — CapiClima: Roadmap Técnico Completo

## Papel e Objetivo

Você é um **engenheiro de software sênior** com experiência em Django, Python e CMS.
Sua tarefa é produzir um **roadmap técnico detalhado** do projeto CapiClima, mapeando todo o fluxo da aplicação — desde o acesso ao Django Admin até cada página pública do site —, incluindo a lógica por trás de cada camada, os modelos do banco de dados, o sistema de permissões e as responsabilidades de cada componente.

---

## Contexto do Projeto

| Atributo             | Valor                                                                 |
| -------------------- | --------------------------------------------------------------------- |
| **Nome**             | CapiClima                                                             |
| **Tipo**             | CMS Django para o Coletivo CapiClima (ONG — Juventude e Meio Ambiente)|
| **Framework**        | Django 5.2                                                            |
| **Linguagem**        | Python 3.11+                                                          |
| **Banco (produção)** | PostgreSQL via `DATABASE_URL`                                         |
| **Banco (dev)**      | SQLite (fallback automático)                                          |
| **Uploads**          | Cloudinary (produção) / armazenamento local `media/` (desenvolvimento)|
| **Rich Text**        | django-ckeditor-5                                                     |
| **Frontend**         | HTML/CSS/JS + Bootstrap 5.3 + Font Awesome 6 + Google Fonts          |

### Estrutura do projeto

```
Capiclima/
├── apps/
│   └── ong/                  ← App principal
│       ├── management/
│       │   └── commands/     ← seed_data, popular_dados
│       ├── migrations/
│       ├── templatetags/
│       │   └── cloudinary_utils.py
│       ├── admin.py
│       ├── apps.py
│       ├── context_processors.py
│       ├── middleware.py
│       ├── models.py
│       ├── permissions.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
├── capiclima/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── static/
│   ├── css/
│   ├── images/
│   └── js/
└── templates/
    ├── includes/
    │   ├── navbar.html
    │   ├── footer.html
    │   └── scripts.html
    └── pages/
        ├── index.html
        ├── sobre.html
        ├── equipe.html
        ├── atividades.html
        ├── oportunidades.html
        └── apoie.html
```

### Modelos conhecidos (`models.py`)

| Model             | Tipo      | Descrição                                                        |
| ----------------- | --------- | ---------------------------------------------------------------- |
| `SiteConfig`      | Singleton | Configuração global: logo, contato, redes sociais, Pix           |
| `SecaoHome`       | Singleton | Conteúdo editável da página inicial (hero, CTA, parceiros)       |
| `SecaoSobre`      | Singleton | Conteúdo da página Sobre (missão, visão, valores)                |
| `SecaoApoie`      | Singleton | Chave Pix e QR Code para doações                                 |
| `SiteSection`     | Multi     | Seções genéricas do site identificadas por slug                  |
| `DestaqueInicio`  | Multi     | Banners/carrosséis da página inicial                             |
| `Parceiro`        | Multi     | Logos e links de parceiros/apoiadores                            |
| `ConteudoSobre`   | Multi     | Blocos de conteúdo da página Sobre                               |
| `Atividade`       | Multi     | Atividades e eventos com data, local, imagem e rich text         |
| `MembroEquipe`    | Multi     | Membros da equipe com foto, bio e links sociais                  |
| `Opportunity`     | Multi     | Oportunidades de voluntariado com controle de expiração por data |

**Padrão Singleton (`SingletonMixin`):** garante exatamente 1 registro por model — `save()` força `pk=1` e `delete()` é bloqueado. Usado em `SiteConfig`, `SecaoHome`, `SecaoSobre` e `SecaoApoie`.

### Sistema de permissões

| Grupo            | Acesso                                                              |
| ---------------- | ------------------------------------------------------------------- |
| **Admin**        | Acesso total ao painel e todos os modelos                           |
| **Colaboradores**| Pode editar conteúdo (seções, atividades, equipe, oportunidades)    |
| Sem grupo        | Recebe página 403 ao tentar acessar `/admin/`                       |

Os grupos são criados automaticamente pelo comando `seed_data`.

---

## Fase 1 — RESEARCH (obrigatória, não pule)

Antes de escrever qualquer coisa, **leia o projeto**. Percorra os arquivos abaixo na ordem indicada:

1. `capiclima/urls.py` — mapeie todas as rotas raiz do projeto
2. `apps/ong/urls.py` — mapeie as rotas do app principal
3. `apps/ong/views.py` — entenda o que cada view faz e quais dados consulta
4. `apps/ong/models.py` — confirme os campos e relações de cada model
5. `apps/ong/admin.py` — mapeie como cada model está registrado, quais são proxy models, quais campos são exibidos e quais filtros/ações existem
6. `apps/ong/permissions.py` — entenda a lógica de controle de acesso
7. `apps/ong/middleware.py` — entenda o que é interceptado antes das views
8. `apps/ong/context_processors.py` — entenda quais dados são injetados globalmente nos templates
9. `apps/ong/templatetags/cloudinary_utils.py` — entenda como as imagens Cloudinary são renderizadas nos templates
10. `apps/ong/management/commands/` — leia `seed_data` e `popular_dados` para entender a população inicial do banco
11. `templates/` — leia todos os templates para entender o que cada página exibe e quais variáveis de contexto consome
12. `capiclima/settings.py` — confirme configurações relevantes (INSTALLED_APPS, MIDDLEWARE, DATABASES, Cloudinary, CKEditor)

> Ao terminar o RESEARCH, você terá uma visão completa e atualizada do projeto. Só então prossiga para a Fase 2.

---

## Fase 2 — ROADMAP

Produza o roadmap no formato abaixo. Cubra **todos** os fluxos listados, na ordem apresentada. Para cada fluxo, explique: o que acontece na camada de entrada (URL/template/Admin), qual view ou lógica é acionada, o que é consultado no banco, e o comportamento esperado para o usuário final.

> O nível de detalhe esperado é: **compreensível para um desenvolvedor que nunca viu o projeto**, sem precisar descrever linha a linha de código.

---

### Estrutura esperada do Roadmap

#### 1. Configuração e Boot do Projeto
- Fluxo de inicialização: `settings.py` → `urls.py` → WSGI/ASGI
- Variáveis de ambiente relevantes e seus efeitos (DEBUG, DATABASE_URL, Cloudinary)
- Fallbacks automáticos (SQLite sem `DATABASE_URL`, `media/` sem Cloudinary)
- Comando `seed_data`: o que cria, o que é idempotente

#### 2. Django Admin — Acesso e Permissões
- URL de acesso (`/admin/`)
- Fluxo de autenticação do Django Admin
- Como o `middleware.py` e `permissions.py` atuam no controle de acesso
- Comportamento por grupo: Admin vs. Colaboradores vs. sem grupo (403)
- Como os proxy models (se existirem) organizam o painel para gestores não-técnicos

#### 3. Django Admin — Gestão de Conteúdo
Para cada model registrado no admin, descreva:
- Nome exibido no painel
- Campos editáveis e campos somente-leitura
- Filtros, buscas e ações disponíveis
- Comportamento especial (Singleton: não pode ser deletado; `Opportunity.esta_aberta`: filtro automático por data)
- Como as imagens Cloudinary são enviadas e armazenadas (pasta por model)
- Validação de extensão de imagem (`image_extension_validator`)

#### 4. Página Inicial (`/`)
- Dados consumidos: `SecaoHome`, `DestaqueInicio`, `Parceiro`, `Atividade` (destaques), `SiteConfig`
- Como o hero, os banners, a seção "Juventudes em Ação", os parceiros e o CTA são montados
- Lógica de destaque de atividades (`destaque=True`)
- Como `context_processors.py` injeta dados globais (ex.: `SiteConfig`) em todos os templates

#### 5. Página Sobre (`/sobre/`)
- Dados consumidos: `SecaoSobre`, `ConteudoSobre`
- Estrutura da página: título, texto principal, missão/visão/valores, blocos de conteúdo
- Renderização de ícones Font Awesome via campo `icone`

#### 6. Página Equipe (`/equipe/`)
- Dados consumidos: `MembroEquipe`
- Ordenação por campo `ordem`
- Fallback de imagem: Cloudinary (`foto`) → estático local (`foto_local`)
- Links sociais (Instagram, LinkedIn)

#### 7. Página Atividades (`/atividades/`)
- Dados consumidos: `Atividade` (apenas `ativo=True`)
- Ordenação por `-data`
- Fallback de imagem: Cloudinary (`imagem`) → estático local (`imagem_local`)
- Campos rich text: `descricao`, `temas_debatidos`, `resultados_encaminhamentos`
- Comportamento de "Ver mais" (expansão de conteúdo)

#### 8. Página Oportunidades (`/oportunidades/`)
- Dados consumidos: `Opportunity`
- Lógica de filtragem automática: `Opportunity.abertas()` (query com `Q` para `data_fim__isnull` ou `data_fim__gte=hoje`)
- Property `esta_aberta`: como é usada no template
- Exibição de datas de inscrição e link de formulário externo

#### 9. Página Apoie (`/apoie/`)
- Dados consumidos: `SecaoApoie`
- Exibição da chave Pix e QR Code
- Por que os demais campos foram removidos do admin (apenas Pix é editável dinamicamente)

#### 10. Navbar, Footer e Componentes Globais
- Dados injetados via `context_processors.py` (ex.: `SiteConfig` com logo, contato, redes sociais)
- Estrutura de includes: `navbar.html`, `footer.html`, `scripts.html`
- Como o `base.html` herda e compõe as páginas

#### 11. Uploads e Imagens (Cloudinary)
- Fluxo completo de upload: Admin → `CloudinaryField` → Cloudinary API → URL retornada
- `cloudinary_utils.py`: como o templatetag transforma o campo em URL renderizável
- Validação de extensão antes do upload
- Fallback para `media/` local quando Cloudinary não está configurado

---

## Restrições e Comportamento Esperado

- **NÃO invente** informações. Se um fluxo não estiver implementado ou não for encontrado no código, registre explicitamente: `> ⚠️ Não encontrado no código — possível TODO.`
- **NÃO gere código** nesta sessão. Apenas mapeie e documente.
- Se encontrar divergências entre o README e o código real, **o código prevalece**. Mencione a divergência no roadmap.
- Use **diagramas de texto simples** (setas `→`, listas hierárquicas) para representar fluxos quando ajudar a clareza.
- O output final deve ser um **documento Markdown estruturado**, pronto para ser salvo como `ROADMAP.md` na raiz do projeto.

---

## Critérios de Aceitação

O roadmap estará completo quando:

- [ ] Todos os 11 fluxos listados estiverem cobertos
- [ ] O sistema de permissões (Admin / Colaboradores / sem grupo) estiver documentado com base no código real
- [ ] O padrão Singleton (`SingletonMixin`) e seus models estiverem explicados
- [ ] O fluxo de imagens Cloudinary (upload → armazenamento → renderização → fallback) estiver descrito
- [ ] A lógica de filtragem de `Opportunity.abertas()` e a property `esta_aberta` estiverem documentadas
- [ ] Nenhuma seção contiver suposições não verificadas no código
- [ ] O documento estiver em Markdown válido, legível e salvo (ou pronto para ser salvo) como `ROADMAP.md`
