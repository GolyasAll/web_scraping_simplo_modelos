from flask import Flask, render_template, request, jsonify
import openpyxl
import threading
import navegador_base
from modulos import simplus, tractor, motos, eletricos

app = Flask(__name__)

# Controle de estado para evitar execuções múltiplas simultâneas
status = {"processando": False}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iniciar_coleta', methods=['POST'])
def iniciar_coleta():
    if status["processando"]:
        return jsonify({"erro": "O robô já está rodando! Acompanhe a janela preta."}), 400
    
    data = request.form
    # Dispara o robô em uma thread separada para não bloquear o servidor web
    threading.Thread(target=processar_robos, args=(data,)).start()
    return jsonify({"mensagem": "Coleta iniciada! Acompanhe o log na janela preta do sistema."})

def processar_robos(data):
    status["processando"] = True
    try:
        wb = openpyxl.Workbook()
        wb.remove(wb.active) # Remove aba padrão vazia
        
        headless = 'headless' in data
        email = data['email']
        senha = data['senha']
        nome_arquivo = data.get('arquivo', 'dados_coletados')
        
        print("\n=== INICIANDO MATRIZ DE COLETA ===")
        navegador = navegador_base.iniciar_sessao(email, senha, headless)
        
        if 'simplus' in data: simplus.rodar(navegador, wb)
        if 'tractor' in data: tractor.rodar(navegador, wb)
        if 'eletricos' in data: eletricos.rodar(navegador, wb)
        if 'motos' in data: motos.rodar(navegador, wb)
        
        wb.save(f"{nome_arquivo}.xlsx")
        print(f"\n=== SUCESSO! Arquivo '{nome_arquivo}.xlsx' salvo. ===")
        
        navegador_base.finalizar_sessao(navegador)
    except Exception as e:
        print(f"\n=== ERRO CRÍTICO NO PROCESSO: {e} ===")
    finally:
        status["processando"] = False

if __name__ == '__main__':
    # Roda o servidor local na porta 5000
    app.run(port=5000, threaded=True)