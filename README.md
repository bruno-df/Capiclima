# CapiClima — CMS Django

Sistema de gerenciamento de conteúdo do Coletivo CapiClima, construído com Django 5.2.

## Requisitos

- Python 3.11+
- pip

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
# Copie o exemplo e edite com seus dados:
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

Acesse o site em `http://localhost:8000/` e o painel em `http://localhost:8000/admin/`.

## Variáveis de ambiente (.env)

| Variável | Obrigatória | Descrição |
|---|---|---|
| `SECRET_KEY` | Sim | Chave secreta do Django |
| `DEBUG` | Não | `True` para desenvolvimento (padrão: `False`) |
| `ALLOWED_HOSTS` | Não | Hosts permitidos, separados por vírgula (padrão: `localhost,127.0.0.1`) |
| `DATABASE_URL` | Não | URL do PostgreSQL. Se vazio, usa SQLite |
| `TIME_ZONE` | Não | Fuso horário (padrão: `America/Cuiaba`) |
| `CLOUDINARY_CLOUD_NAME` | Não | Nome do cloud no Cloudinary |
| `CLOUDINARY_API_KEY` | Não | Chave da API do Cloudinary |
| `CLOUDINARY_API_SECRET` | Não | Secret da API do Cloudinary |
| `CSRF_TRUSTED_ORIGINS` | Não | Origens confiáveis para CSRF em produção |

Se as variáveis do Cloudinary não estiverem configuradas, o sistema usa armazenamento local (`media/`).

## Estrutura do CMS

### Modelos principais

- **SiteConfig** — Configuração global (logo, contato, redes sociais, Pix). Singleton, editável via admin.
- **SiteSection** — Seções editáveis do site (hero, textos, CTAs). Identificadas por slug.
- **Opportunity** — Oportunidades de voluntariado com datas e filtro automático de expiração.
- **Atividade** — Atividades e eventos com data, local, imagem e rich text.
- **MembroEquipe** — Membros da equipe com foto, bio e links sociais.
- **DestaqueInicio** — Banners do hero da página inicial.
- **ConteudoSobre** — Blocos de conteúdo da página Sobre.

### Permissões

| Grupo | Acesso |
|---|---|
| **Admin** | Acesso total ao painel e todos os modelos |
| **Colaboradores** | Pode editar conteúdo do site (seções, atividades, equipe, oportunidades) |
| Sem grupo | Recebe página 403 ao tentar acessar `/admin/` |

Os grupos são criados automaticamente pelo comando `seed_data`.

### Comandos úteis

```bash
# Popular banco com dados iniciais (idempotente)
python manage.py seed_data

# Popular com dados do comando antigo (apenas equipe/atividades)
python manage.py popular_dados

# Verificar integridade do projeto
python manage.py check

# Criar migrações após alterações nos models
python manage.py makemigrations
python manage.py migrate
```

## Deploy em produção

1. Configure `DEBUG=False` no `.env`
2. Defina `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS`
3. Configure `SECRET_KEY` com um valor seguro (use `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
4. Configure `DATABASE_URL` para PostgreSQL
5. Configure Cloudinary para uploads em produção
6. Execute `python manage.py collectstatic`
7. Use Gunicorn + Nginx ou plataforma como Render/Railway

## Tecnologias

- **Backend:** Django 5.2
- **Frontend:** HTML/CSS/JS + Bootstrap 5.3 + Font Awesome 6
- **Editor Rich Text:** django-ckeditor-5
- **Upload de imagens:** Cloudinary (produção) / Local (desenvolvimento)
- **Banco de dados:** PostgreSQL (produção) / SQLite (desenvolvimento)
- **Fontes:** Google Fonts (Inter + Outfit)
