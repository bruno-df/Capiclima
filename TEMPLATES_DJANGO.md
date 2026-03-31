# 📱 Documentação dos Templates Django - CapiClima

## 📁 Estrutura de Templates

```
templates/
├── base.html                    # Template base (herança)
├── includes/
│   ├── navbar.html             # Barra de navegação ({% include %})
│   ├── footer.html             # Rodapé ({% include %})
│   └── scripts.html            # Scripts JS ({% include %})
└── pages/
    ├── index.html              # Página inicial
    ├── sobre.html              # Sobre o CapiClima
    ├── atividades.html         # Atividades
    ├── oportunidades.html      # Oportunidades de voluntariado
    └── apoie.html              # Como apoiar
```

---

## 🔍 Como Funcionam os Includes

### **Template Base (base.html)**

```django
{% extends "base.html" %}
{% load static %}

{% block title %}Página Inicial{% endblock %}
{% block meta_description %}Descrição da página{% endblock %}

{% block content %}
    <!-- Conteúdo específico da página -->
{% endblock %}

{% block extra_css %}
    <!-- CSS específico desta página (opcional) -->
{% endblock %}

{% block extra_js %}
    <!-- JS específico desta página (opcional) -->
{% endblock %}
```

### **Includes Usados em base.html**

```django
{# Barra de Navegação #}
{% include "includes/navbar.html" %}

{# Conteúdo renderizado pelas páginas filhas #}
<main>
    {% block content %}{% endblock %}
</main>

{# Rodapé #}
{% include "includes/footer.html" %}

{# Scripts (Bootstrap, jQuery, Font Awesome) #}
{% include "includes/scripts.html" %}
```

---

## 📄 Páginas Disponíveis

### 1️⃣ **index.html** - Página Inicial
- **URL:** `http://localhost:8000/`
- **View:** `IndexView`
- **Template Tag:** `{% url 'index' %}`
- Exibe carousel com últimas atividades
- Botão "Saiba Mais" para `/sobre/`

### 2️⃣ **sobre.html** - Sobre o CapiClima
- **URL:** `http://localhost:8000/sobre/`
- **View:** `SobreView`
- **Template Tag:** `{% url 'sobre' %}`
- Informações sobre a organização
- Números de impacto

### 3️⃣ **atividades.html** - Atividades
- **URL:** `http://localhost:8000/atividades/`
- **View:** `AtividadesView`
- **Template Tag:** `{% url 'atividades' %}`
- Galeria de atividades
- Filtro por ano (2024, 2025)
- JavaScript para filtros

### 4️⃣ **oportunidades.html** - Voluntariado
- **URL:** `http://localhost:8000/oportunidades/`
- **View:** `OportunidadesView`
- **Template Tag:** `{% url 'oportunidades' %}`
- 4 oportunidades de voluntariado
- Links para candidaturas via email

### 5️⃣ **apoie.html** - Como Apoiar
- **URL:** `http://localhost:8000/apoie/`
- **View:** `ApoieView`
- **Template Tag:** `{% url 'apoie' %}`
- Formas de apoio (voluntariado, doação, parcerias)
- CTAs para contato

---

## 🔗 Tags Django Importantes

### **{% load static %}**
Carrega a tag `{% static %}` para servir arquivos estáticos.

```django
{% load static %}
<img src="{% static 'images/logo/logo.png' %}" alt="Logo">
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script src="{% static 'js/include.js' %}"></script>
```

### **{% url 'name' %}**
Gera URLs dinamicamente baseadas nos nomes definidos em `urls.py`.

```django
{# Em urls.py #}
path('', views.IndexView.as_view(), name='index')

{# Em templates #}
<a href="{% url 'index' %}">Voltar para Início</a>
```

### **{% extends "base.html" %}**
Herança de templates - estende o template pai.

```django
{% extends "base.html" %}

{% block content %}
    {# Conteúdo específico desta página #}
{% endblock %}
```

### **{% include "includes/navbar.html" %}**
Inclui um template dentro de outro.

```django
{% include "includes/navbar.html" %}
{# Renderiza o conteúdo de navbar.html aqui #}
```

### **{% block content %} ... {% endblock %}**
Define uma área que pode ser sobrescrita por templates filhos.

```django
{# Em base.html #}
{% block content %}
    {# Conteúdo padrão #}
{% endblock %}

{# Em pages/index.html #}
{% block content %}
    {# Sobrescreve o conteúdo padrão #}
{% endblock %}
```

---

## 🎨 Componentes Reutilizáveis

### **Barra de Navegação (navbar.html)**
- Menu responsivo com Bootstrap
- Links dinâmicos usando `{% url %}`
- Logo do CapiClima
- Botão "Apoie" destacado

### **Rodapé (footer.html)**
- Links de redes sociais
- Informações de contato
- Copyright
- Links são clicáveis (mailto:, tel:, https://)

### **Scripts (scripts.html)**
- Bootstrap 4 (JS + CSS)
- jQuery
- Popper.js
- Font Awesome (ícones)
- Scripts personalizados

---

## 📱 Responsividade

Todos os templates usam **Bootstrap 4** para responsividade:

```django
<div class="container">           {# Contêiner da página #}
    <div class="row">             {# Linha de 12 colunas #}
        <div class="col-md-6">    {# 6 colunas em md+, full em xs-sm #}
            Conteúdo
        </div>
    </div>
</div>
```

---

## 🚀 Como Adicionar uma Nova Página

### 1. Criar o template em `templates/pages/nova_pagina.html`

```django
{% extends "base.html" %}
{% load static %}

{% block title %}Nova Página - CapiClima{% endblock %}
{% block meta_description %}Descrição da nova página{% endblock %}

{% block content %}
    <div class="container py-5">
        <h1>Título da Página</h1>
        <!-- Conteúdo aqui -->
    </div>
{% endblock %}
```

### 2. Criar a view em `apps/ong/views.py`

```python
class NovaPaginaView(TemplateView):
    """Descrição da página"""
    template_name = 'pages/nova_pagina.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nova Página'
        return context
```

### 3. Adicionar a rota em `apps/ong/urls.py`

```python
path('nova-pagina/', views.NovaPaginaView.as_view(), name='nova_pagina'),
```

### 4. Usar em templates

```django
<a href="{% url 'nova_pagina' %}">Link para Nova Página</a>
```

---

## 🔐 Context Variables

Toda view passa variáveis de contexto para seus templates:

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Título da Página'
    context['description'] = 'Descrição'
    context['items'] = Item.objects.all()
    return context
```

Usar em template:
```django
<h1>{{ title }}</h1>
<p>{{ description }}</p>
{% for item in items %}
    <p>{{ item }}</p>
{% endfor %}
```

---

## ✅ Checklist Django Templates

- ✅ `{% load static %}` no início do template
- ✅ `{% extends "base.html" %}` para herança
- ✅ `{% url 'name' %}` para links dinâmicos
- ✅ `{% include "..." %}` para componentes
- ✅ `{% block %}` para áreas customizáveis
- ✅ `{% for item in items %} ... {% endfor %}` para loops
- ✅ `{% if condition %} ... {% endif %}` para condicionais
- ✅ `{{ variable }}` para mostrar variáveis

---

## 🔗 Referências

- [Django Templates Docs](https://docs.djangoproject.com/en/6.0/topics/templates/)
- [Bootstrap 4 Docs](https://getbootstrap.com/docs/4.6/)
- [Font Awesome Icons](https://fontawesome.com/)

