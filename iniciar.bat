@echo off
title Sistema Simplo Online

echo =========================================
echo VERIFICANDO AMBIENTE...
echo =========================================

:: Tenta usar 'python' ou 'py' para criar a venv
if not exist venv (
    echo Criando ambiente virtual...
    python -m venv venv || py -m venv venv
)

:: Ativa o ambiente virtual
call venv\Scripts\activate

echo.
echo Instalando dependencias...
pip install flask openpyxl selenium

echo.
echo Iniciando o sistema (Acesse http://127.0.0.1:5000 no navegador)...
start http://127.0.0.1:5000

:: Inicia o app.py usando o python do ambiente virtual ativado
python app.py

pause