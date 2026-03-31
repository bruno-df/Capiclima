# CapiClima - Website

## Sobre o Projeto

**Projeto de Sistema Web para Instituição Filantrópica - IFMT**

- **Instituição**: Coletivo CapiClima
- **Equipe**: Bruno Fonteles, Lucas Gomes e Gabriel Mallezan
- **Orientador**: Me. Rafael Rocha
- **Curso**: Sistemas para Internet (4º semestre) - IFMT Campus Cuiabá

### Sobre o CapiClima
- Criado em abril de 2024
- 11 membros voluntários
- Atua nas áreas de juventude, educação e meio ambiente
- Objetivo: ampliar rede e ações até 2026

---

## Estrutura do Projeto

Este é um projeto **Django** com a seguinte organização:

```
capiclima/
├── manage.py                 # Comando principal do Django
├── requirements.txt          # Dependências Python
├── capiclima/               # Configurações do projeto
│   ├── settings.py          # Configurações principais
│   ├── urls.py              # URLs principais
│   ├── wsgi.py              # Interface WSGI
│   └── asgi.py              # Interface ASGI
├── apps/                    # Aplicações Django
│   └── ong/                 # App da ONG
│       ├── models.py
│       ├── views.py
│       ├── admin.py
│       └── migrations/
├── templates/               # Templates HTML
│   ├── index.html
│   ├── sobre.html
│   ├── atividades.html
│   ├── oportunidades.html
│   ├── apoie.html
│   └── includes/            # Componentes reutilizáveis
│       ├── navbar.html
│       └── footer.html
├── static/                  # Arquivos estáticos
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── include.js
│   └── images/
│       ├── atividades/
│       ├── geral/
│       ├── gestao/
│       ├── icones/
│       └── logo/
└── .env                     # Variáveis de ambiente

```

---

## Setup e Instalação

### 1. Criar ambiente virtual
```bash
python -m venv .venv
```

### 2. Ativar ambiente virtual
**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente
Copie `.env` e configure com seus valores:
```bash
SECRET_KEY=sua_chave_secreta
DEBUG=True
DATABASE_URL=sua_url_do_banco
```

### 5. Executar migrações
```bash
python manage.py migrate
```

### 6. Criar superuser (admin)
```bash
python manage.py createsuperuser
```

### 7. Rodar servidor de desenvolvimento
```bash
python manage.py runserver
```

Acesse: http://localhost:8000/

---

## Tecnologias

- **Python 3.x**
- **Django 6.0.3**
- **PostgreSQL** (via Supabase)
- **HTML5 / CSS3**
- **JavaScript**

---

## Comandos Úteis

| Comando | Descrição |
|---------|-----------|
| `python manage.py runserver` | Inicia servidor de desenvolvimento |
| `python manage.py migrate` | Aplica migrações do banco |
| `python manage.py makemigrations` | Cria novas migrações |
| `python manage.py createsuperuser` | Cria usuário administrador |
| `python manage.py collectstatic` | Coleta arquivos estáticos |
| `python manage.py shell` | Abre shell interativo do Django |

---

## Contribuindo

1. Crie uma branch para sua funcionalidade
2. Faça commit de suas mudanças
3. Envie um pull request

---

## Licença

Este projeto é desenvolvido como parte das atividades do Instituto Federal de Mato Grosso (IFMT).