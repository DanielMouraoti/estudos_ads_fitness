#!/bin/bash
echo "[*] Criando ambiente virtual..."
python3 -m venv venv_treino

echo "[*] Ativando ambiente e instalando bibliotecas..."
source venv_treino/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "[*] Configurando dependências do Browser (Playwright)..."
playwright install chromium

echo "[OK] Setup concluído! Para começar, use: source venv_treino/bin/activate"
