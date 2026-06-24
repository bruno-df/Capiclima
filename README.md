# CapiClima — CMS Django

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)

Sistema de gerenciamento de conteúdo do **Coletivo CapiClima**, construído com Django. Permite que gestores não-técnicos editem todas as páginas públicas do site — atividades, equipe, oportunidades, parceiros e configurações — diretamente pelo painel administrativo.

O Coletivo CapiClima é uma organização voluntária que mobiliza juventudes para ações de educação ambiental e justiça climática em Mato Grosso.

---

## Stack

| Componente        | Tecnologia                           | Versão   |
|-------------------|--------------------------------------|----------|
| Framework         | Django                               | 5.2.15   |
| Linguagem         | Python                               | 3.11+    |
| Banco (produção)  | PostgreSQL via `dj-database-url`     | —        |
| Banco (dev)       | SQLite (fallback automático)         | —        |
| Upload de mídia   | Cloudinary / Local (fallback)        | 1.40.0   |
| Rich Text         | django-ckeditor-5                    | 0.2.20   |
| Admin Theme       | django-jazzmin                       | —        |
| Processamento img | Pillow                               | 12.2.0   |
| Frontend          | Bootstrap 5.3 + Font Awesome 6 + Google Fonts (Inter, Outfit) | —        |

---

## Funcionalidades

- **6 páginas públicas** gerenciáveis via painel admin: Início, Sobre, Equipe, Atividades, Oportunidades e Apoie
- **Sistema de permissões por grupo** — Admin (acesso total) e Colaboradores (edição de conteúdo)
- **Upload de imagens via Cloudinary** com validação de extensão (`jpg`, `jpeg`, `png`, `webp`) e fallback automático para armazenamento local
- **Modelos Singleton** para configurações globais (SiteConfig, SecaoHome, SecaoSobre, SecaoApoie) — sem risco de duplicação
- **Controle de expiração automático** de oportunidades por data (`Opportunity.abertas()`)
- **Rich text (CKEditor 5)** nos campos de conteúdo de atividades, seções e oportunidades
- **Contadores animados** na home e página Sobre, com polling em tempo real via API JSON
- **Comando `seed_data`** para popular o banco com dados iniciais (idempotente)
- **Carrossel de destaques** na página inicial com suporte a botões e links configuráveis
- **Filtro de atividades por ano** com paginação (9 por página)

---

## Pré-requisitos

- Python 3.11+
- pip
- (Opcional) Conta no [Cloudinary](https://cloudinary.com/) para uploads em produção

---

## Setup local

```bash
# 1. Clone o repositório
git clone https://github.com/bruno-df/Capiclima.git
cd Capiclima

# 2. Crie e ative um ambiente virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Preencha pelo menos SECRET_KEY e DEBUG=True

# 5. Aplique as migrações
python manage.py migrate

# 6. Popule o banco com dados iniciais
python manage.py seed_data

# 7. Crie um superusuário
python manage.py createsuperuser

# 8. Rode o servidor de desenvolvimento
python manage.py runserver
```

- **Site:** `http://localhost:8000/`
- **Admin:** `http://localhost:8000/admin/`

---

## Variáveis de ambiente

Copie `.env.example` para `.env` e configure conforme necessário.

| Variável                | Obrigatória | Descrição                                                                 |
|-------------------------|-------------|---------------------------------------------------------------------------|
| `SECRET_KEY`           | Sim         | Chave secreta do Django. Obrigatória — o projeto não inicia sem ela.      |
| `DEBUG`                | Não         | `True` para desenvolvimento. Padrão: `False`.                             |
| `ALLOWED_HOSTS`        | Não         | Hosts permitidos, separados por vírgula. Padrão: `localhost,127.0.0.1`.   |
| `TIME_ZONE`            | Não         | Fuso horário. Padrão: `America/Cuiaba`.                                   |
| `DATABASE_URL`         | Não         | URL do PostgreSQL (ex: `postgres://user:pass@host:5432/db`). Se vazio, usa SQLite local (`db.sqlite3`). |
| `CLOUDINARY_CLOUD_NAME`| Não         | Nome do cloud no Cloudinary.                                              |
| `CLOUDINARY_API_KEY`   | Não         | Chave da API do Cloudinary.                                               |
| `CLOUDINARY_API_SECRET`| Não         | Secret da API do Cloudinary.                                              |
| `CSRF_TRUSTED_ORIGINS` | Não         | Origens confiáveis para CSRF em produção (ex: `https://seudominio.com`).  |

**Fallbacks automáticos:**
- Sem `DATABASE_URL` → SQLite em `db.sqlite3` na raiz do projeto.
- Sem as 3 variáveis Cloudinary → armazenamento local em `media/` (servido automaticamente em `DEBUG=True`).

---

## Estrutura do projeto

```
Capiclima/
├── apps/
│   └── ong/                        ← App principal do CMS
│       ├── management/
│       │   └── commands/           ← seed_data, popular_dados, migrate_sitesection
│       ├── migrations/
│       ├── templatetags/
│       │   └── cloudinary_utils.py ← Filtro de otimização de URLs Cloudinary
│       ├── admin.py                ← Registro e configuração dos modelos no admin
│       ├── apps.py
│       ├── context_processors.py   ← Injeta SiteConfig em todos os templates
│       ├── middleware.py           ← Controle de acesso ao /admin/ por grupo
│       ├── models.py              ← Todos os modelos do CMS
│       ├── permissions.py         ← Lógica de permissões e criação de grupos
│       ├── urls.py                ← Rotas do app (6 páginas + API de stats)
│       └── views.py               ← Views das páginas públicas
├── capiclima/
│   ├── settings.py                ← Configurações do projeto
│   ├── urls.py                    ← Rotas raiz (/admin/, /ckeditor5/, app)
│   ├── wsgi.py
│   └── asgi.py
├── static/
│   ├── css/                       ← Estilos personalizados
│   ├── images/                    ← Imagens estáticas (logos, SVGs, fallbacks)
│   └── js/                        ← Scripts (navbar mobile, contadores animados)
├── templates/
│   ├── base.html                  ← Template base (head, navbar, footer, scripts)
│   ├── 403.html                   ← Página de acesso negado
│   ├── includes/                  ← Componentes reutilizáveis (navbar, footer, scripts)
│   └── pages/                     ← Templates das 6 páginas públicas
├── .env.example
├── manage.py
└── requirements.txt
```

---

## Modelos do banco

| Model            | Tipo      | Descrição                                                         |
|------------------|-----------|-------------------------------------------------------------------|
| `SiteConfig`     | Singleton | Configuração global: nome, logo, favicon, contato, redes sociais  |
| `SecaoHome`      | Singleton | Conteúdo editável da página inicial (hero, juventudes, CTA, parceiros) |
| `SecaoSobre`     | Singleton | Conteúdo da página Sobre (título, texto, missão, visão, valores)  |
| `SecaoApoie`     | Singleton | Chave Pix e QR Code para doações                                  |
| `SiteSection`    | Multi     | Seções genéricas do site identificadas por slug (legado)           |
| `DestaqueInicio` | Multi     | Banners/slides do carrossel da página inicial                      |
| `Parceiro`       | Multi     | Logos e links de parceiros/apoiadores                              |
| `ConteudoSobre`  | Multi     | Blocos de conteúdo da página Sobre (ícone + texto + imagem)        |
| `Atividade`      | Multi     | Atividades e eventos com data, local, imagem e rich text           |
| `MembroEquipe`   | Multi     | Membros da equipe com foto, bio e links sociais                    |
| `Opportunity`    | Multi     | Oportunidades de voluntariado com controle de expiração por data   |

**Padrão Singleton (`SingletonMixin`):** garante exatamente 1 registro por modelo — `save()` força `pk=1`, `delete()` é bloqueado, e `load()` usa `get_or_create(pk=1)`. Aplicado em `SiteConfig`, `SecaoHome`, `SecaoSobre` e `SecaoApoie`.

---

## Permissões e Admin

| Grupo             | Acesso                                                              |
|-------------------|---------------------------------------------------------------------|
| **Admin**         | Acesso total ao painel e todos os modelos                           |
| **Colaboradores** | Edição de conteúdo: atividades, equipe, oportunidades, seções, configurações |
| Sem grupo (staff) | Página 403 ao tentar acessar `/admin/`                              |

- Os grupos são criados automaticamente pelo comando `seed_data` (via `sync_cms_groups()`).
- O middleware `AdminGroupRequiredMiddleware` intercepta `/admin/` e `/ckeditor5/` e verifica se o usuário pertence a um dos grupos autorizados.
- **Acesso ao painel:** `http://localhost:8000/admin/`
- **Tema:** Jazzmin (tema `flatly`, sidebar verde, ícones customizados por modelo).

---

## Comandos úteis

| Comando                              | Descrição                                                    |
|--------------------------------------|--------------------------------------------------------------|
| `python manage.py seed_data`        | Popula o banco com dados iniciais — idempotente               |
| `python manage.py popular_dados`    | Popula equipe e atividades (comando legado, mais detalhado)   |
| `python manage.py migrate_sitesection` | Migra dados de SiteSection para os modelos dedicados       |
| `python manage.py makemigrations`   | Cria migrações após alterações nos models                     |
| `python manage.py migrate`          | Aplica migrações pendentes                                    |
| `python manage.py collectstatic`    | Coleta arquivos estáticos para produção                       |
| `python manage.py check`            | Verifica integridade do projeto                               |

---

## Deploy em produção

1. Configure `DEBUG=False` no `.env`
2. Defina `ALLOWED_HOSTS` com o domínio do site
3. Defina `CSRF_TRUSTED_ORIGINS` com a URL completa (ex: `https://seudominio.com`)
4. Gere uma `SECRET_KEY` segura:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
5. Configure `DATABASE_URL` apontando para PostgreSQL
6. Configure as variáveis Cloudinary (`CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`)
7. Execute `python manage.py collectstatic`
8. Sirva a aplicação com um servidor WSGI (ex: Gunicorn)
