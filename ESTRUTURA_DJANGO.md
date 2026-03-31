# Estrutura do Projeto Django - CapiClima

## 📁 Organização Padrão

A seguir está a estrutura reorganizada do projeto seguindo as melhores práticas Django:

```
capiclima/
│
├── capiclima/                    # Configurações do Projeto
│   ├── __init__.py
│   ├── settings.py              # Configurações principais (BD, apps, etc)
│   ├── urls.py                  # URL routing principal
│   ├── wsgi.py                  # Interface WSGI (produção)
│   └── asgi.py                  # Interface ASGI (async)
│
├── apps/                        # Aplicações Django
│   └── ong/                     # Aplicação principal (ONG)
│       ├── migrations/          # Histórico de alterações no BD
│       ├── __init__.py
│       ├── admin.py             # Painel administrativo
│       ├── apps.py              # Configuração da app
│       ├── models.py            # Modelos de dados
│       ├── views.py             # Lógica de visualização
│       ├── urls.py              # URLs da app (quando necessário)
│       └── tests.py             # Testes unitários
│
├── static/                      # Arquivos estáticos
│   ├── css/
│   │   └── style.css           # Estilos principais
│   ├── js/
│   │   └── include.js          # Scripts JavaScript
│   └── images/
│       ├── atividades/         # Fotos de atividades
│       ├── geral/              # Imagens gerais
│       ├── gestao/             # Imagens de gestão
│       ├── icones/             # Ícones
│       └── logo/               # Logotipos
│
├── templates/                   # Templates HTML (renderizados dinamicamente)
│   ├── index.html              # Página inicial
│   ├── sobre.html              # Sobre
│   ├── atividades.html         # Atividades
│   ├── oportunidades.html      # Oportunidades
│   ├── apoie.html              # Como apoiar
│   └── includes/               # Componentes reutilizáveis
│       ├── navbar.html         # Barra de navegação
│       └── footer.html         # Rodapé
│
├── media/                       # Uploads de usuários (criado automaticamente)
│
├── staticfiles/                 # Arquivos colmatados (produção)
│
├── manage.py                    # Comando principal Django
├── requirements.txt             # Dependências Python
├── .env                         # Variáveis de ambiente (NÃO commitar)
├── .env.example                 # Exemplo de variáveis (commitar)
├── README.md                    # Documentação do projeto
└── .gitignore                   # Ignora arquivos desnecessários
```

---

## 🔄 Mudanças Realizadas

### 1️⃣ **Reorganização de Pastas**
- ✅ `core/` → `capiclima/` (configurações do projeto)
- ✅ `ong/` → `apps/ong/` (aplicações dentro de uma pasta `apps/`)
- ✅ `js/` → `static/js/` (arquivos estáticos centralizados)
- ✅ `images/` → `static/images/` (imagens em estáticos)
- ✅ `style.css` → `static/css/style.css`
- ✅ `inject/` → `templates/includes/` (componentes HTML)
- ✅ HTML files → `templates/` (templates renderizáveis)

### 2️⃣ **Atualização de Configurações**
- ✅ `manage.py`: Atualizado para usar `capiclima.settings`
- ✅ `settings.py`:
  - `ROOT_URLCONF` → `capiclima.urls`
  - `WSGI_APPLICATION` → `capiclima.wsgi.application`
  - `INSTALLED_APPS` → Adicionado `apps.ong`
  - `TEMPLATES['DIRS']` → Adicionado `BASE_DIR / 'templates'`
  - `STATIC_URL` e `STATICFILES_DIRS` → Configurados corretamente
  - `MEDIA_URL` e `MEDIA_ROOT` → Adicionados para uploads
  - Idioma/Timezone → `pt-br` e `America/Argentina/Salta`

### 3️⃣ **Novos Arquivos**
- ✅ `.env.example` - Template de variáveis de ambiente
- ✅ README.md atualizado com documentação completa

---

## 🚀 Próximos Passos

1. **Testar o servidor:**
   ```bash
   python manage.py runserver
   ```

2. **Verificar migrações:**
   ```bash
   python manage.py migrate
   ```

3. **Criar superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```

4. **Adicionar URLs da app (se necessário):**
   - Criar `apps/ong/urls.py`
   - Incluir em `capiclima/urls.py`

---

## 📝 Comandos Úteis

```bash
# Verificar se está tudo bem configurado
python manage.py check

# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar usuário admin
python manage.py createsuperuser

# Coletar arquivos estáticos (produção)
python manage.py collectstatic --noinput

# Abrir shell do Django
python manage.py shell

# Rodar testes
python manage.py test
```

---

## ⚠️ Importante

- **Nunca commitar `.env`** - usar `.env.example` como referência
- Manter estrutura de `apps/` para futuras aplicações (melhor escalabilidade)
- Usar `templates/includes/` para componentes reutilizáveis
- Arquivo de estáticos devem ficar sempre em `static/`

