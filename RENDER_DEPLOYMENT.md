# Configuração do Capiclima no Render

## ✅ Já configurado no código:

- ✓ Gunicorn adicionado ao `requirements.txt`
- ✓ WhiteNoise configurado para servir arquivos estáticos
- ✓ Segurança (HTTPS, cookies seguros) para produção
- ✓ Static files com compressão
- ✓ Database via `DATABASE_URL`
- ✓ Cloudinary para mídia

---

## 🚀 Próximos passos no Render

### 1. **Criar um novo Web Service no Render**
   - Acesse [render.com](https://render.com)
   - Clique em "New +" → "Web Service"
   - Conecte seu repositório GitHub

### 2. **Configurar os campos do Web Service**

| Campo | Valor |
|-------|-------|
| **Name** | `capiclima` (ou outro nome disponível) |
| **Language** | Python 3 |
| **Branch** | `capi2` |
| **Region** | Oregon (US West) |
| **Root Directory** | Deixe vazio |
| **Build Command** | `pip install -r requirements.txt && python manage.py collectstatic --noinput` |
| **Start Command** | `gunicorn capiclima.wsgi:application` |
| **Instance Type** | Free |

### 3. **Configurar as variáveis de ambiente**

Na aba **Environment Variables**, adicione todas essas variáveis:

```
DEBUG=False
SECRET_KEY=sua_chave_secreta_aqui
ALLOWED_HOSTS=capiclima.onrender.com
CSRF_TRUSTED_ORIGINS=https://capiclima.onrender.com
DATABASE_URL=postgresql://usuario:senha@hostname:5432/database
CLOUDINARY_CLOUD_NAME=seu_cloud_name
CLOUDINARY_API_KEY=sua_api_key
CLOUDINARY_API_SECRET=seu_api_secret
TIME_ZONE=America/Cuiaba
```

### 4. **Criar um banco de dados PostgreSQL (se não tiver)**
   - No Render, clique em "New +" → "PostgreSQL"
   - Deixe as opções padrão
   - Copie a `DATABASE_URL` fornecida
   - Cole no Web Service

### 5. **Fazer deploy**
   - Clique em "Create Web Service"
   - O Render fará o build automaticamente
   - Acompanhe os logs para ver se há erros

---

## 🔧 Troubleshooting comum

### Erro: "Could not open requirements file: No such file or directory: 'requirements.txt'"
**Causa mais comum:** o Render está apontando para a branch errada. Neste projeto, a aplicação Django está na branch `capi2`; a branch `main` no GitHub não tem `requirements.txt`.

**Solução:** no Render, configure o Web Service para usar a branch `capi2`. Se preferir usar `main`, primeiro faça merge da branch `capi2` para `main` e envie para o GitHub.

### Erro: "No module named 'gunicorn'"
**Solução:** Execute `pip install gunicorn` localmente e `pip freeze > requirements.txt`

### Erro: "Static files not found"
**Solução:** Já está configurado com WhiteNoise. Se persistir, execute no terminal Render:
```bash
python manage.py collectstatic --noinput
```

### Erro: "ALLOWED_HOSTS"
**Solução:** Certifique-se que a variável `ALLOWED_HOSTS` inclui o domínio do Render

### Erro de conexão com banco de dados
**Solução:** Verifique se `DATABASE_URL` está correta e se o PostgreSQL está conectado

### Erro: "SECRET_KEY not found"
**Solução:** Adicione `SECRET_KEY` nas Environment Variables do Render

---

## 📋 Checklist final

- [ ] Gunicorn adicionado ao `requirements.txt` ✓
- [ ] WhiteNoise configurado ✓
- [ ] Security settings configurados ✓
- [ ] Variáveis de ambiente criadas no Render
- [ ] PostgreSQL criado e DATABASE_URL configurado
- [ ] Cloudinary credentials adicionadas
- [ ] Build Command testado localmente
- [ ] Deploy realizado e testado em produção

---

## 🌐 URLs úteis

- Dashboard Render: https://dashboard.render.com
- Documentação Render Python: https://render.com/docs/deploy-django
- Seu site: `https://capiclima.onrender.com`

