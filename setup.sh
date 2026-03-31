#!/bin/bash
# Setup automático para projeto Django CapiClima
# Compatível com Linux e macOS

echo ""
echo "========================================"
echo "CapiClima - Django Setup"
echo "========================================"
echo ""

# 1. Criar ambiente virtual
echo "[1/5] Criando ambiente virtual..."
if [ -d ".venv" ]; then
    echo "Ambiente virtual já existe!"
else
    python3 -m venv .venv
    echo "✓ Ambiente virtual criado"
fi

# 2. Ativar ambiente virtual
echo ""
echo "[2/5] Ativando ambiente virtual..."
source .venv/bin/activate
echo "✓ Ambiente virtual ativado"

# 3. Instalar dependências
echo ""
echo "[3/5] Instalando dependências..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
echo "✓ Dependências instaladas"

# 4. Executar migrações
echo ""
echo "[4/5] Executando migrações do banco de dados..."
python manage.py migrate
echo "✓ Banco de dados atualizado"

# 5. Criar superuser (opcional)
echo ""
echo "[5/5] Criação de usuário administrador"
echo "Digite suas informações abaixo:"
python manage.py createsuperuser

echo ""
echo "========================================"
echo "✓ Setup concluído com sucesso!"
echo "========================================"
echo ""
echo "Para iniciar o servidor de desenvolvimento, execute:"
echo "  python manage.py runserver"
echo ""
echo "Acesse: http://localhost:8000/"
echo "Admin: http://localhost:8000/admin/"
echo ""
