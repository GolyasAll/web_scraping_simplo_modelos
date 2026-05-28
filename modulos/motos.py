import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import clicar_menu_exato

def rodar(navegador, wb):
    """Executa a coleta de dados do pacote Motos e grava na aba do Excel"""
    try:
        # Cria a aba EXCLUSIVA deste pacote no Excel
        aba = wb.create_sheet("Motos")
        aba.append(['Pacote', 'Manual', 'Submanual', 'Montadora', 'Modelo'])

        print("Garantindo pacote 'Motos'...")
        for tentativa in range(2):
            botao_motos = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//img[@alt='motorcycle']"))
            )
            navegador.execute_script("arguments[0].click();", botao_motos)
            time.sleep(3) 
            
            teste_menu = navegador.find_elements(By.XPATH, "//aside[1]//*[contains(text(), 'CÓDIGO DE FALHAS')]")
            if len(teste_menu) > 0:
                break

        estrutura_manuais = {
            "CÓDIGO DE FALHAS": [],
            "ELECTRA": [],
            "INJEÇÂO ELETRÔNICA": [],
            "LUBRITEC": [],
            "MOTORES": [],
        }

        for nome_manual, lista_submanuais in estrutura_manuais.items():
            print(f"\n==========================================")
            print(f"ABRINDO MANUAL PRINCIPAL: {nome_manual}")
            print(f"==========================================")

            sucesso_manual = clicar_menu_exato(navegador, nome_manual, tempo_maximo=10)
            if not sucesso_manual:
                print(f"  [AVISO] Manual '{nome_manual}' não encontrado nesta versão. Pulando...")
                continue 

            time.sleep(1.5) 

            lista_para_raspar = lista_submanuais if len(lista_submanuais) > 0 else ["-"]

            for nome_submanual in lista_para_raspar:
                if nome_submanual != "-":
                    print(f"\n  >>> Acessando Submanual: {nome_submanual}")
                    sucesso_sub = clicar_menu_exato(navegador, nome_submanual, tempo_maximo=10)
                    if not sucesso_sub:
                        print(f"  [AVISO] Submanual '{nome_submanual}' não encontrado. Pulando...")
                        continue
                    time.sleep(2) 
                else:
                    print(f"\n  >>> Manual direto (sem submanuais). Iniciando varredura...")
                
                print("  Aguardando a lista de montadoras...")
                xpath_caixa_montadoras = "//div[contains(@class, 'sc-dWRHGJ')]"
                
                try:
                    WebDriverWait(navegador, 5).until(
                        EC.presence_of_element_located((By.XPATH, f"{xpath_caixa_montadoras}//div[contains(@class, 'menu-item')]"))
                    )
                except:
                    print(f"  [AVISO] Nenhuma montadora encontrada. Pulando...")
                    continue 
                
                caixa_montadoras = navegador.find_element(By.XPATH, xpath_caixa_montadoras)
                lista_inicial = caixa_montadoras.find_elements(By.XPATH, ".//div[contains(@class, 'menu-item')]")
                qtd_montadoras = len(lista_inicial)
                
                for i in range(qtd_montadoras):
                    caixa_atualizada = navegador.find_element(By.XPATH, xpath_caixa_montadoras)
                    montadoras_atualizadas = caixa_atualizada.find_elements(By.XPATH, ".//div[contains(@class, 'menu-item')]")
                    montadora_atual = montadoras_atualizadas[i]
                    nome_montadora = montadora_atual.text.strip()
                    
                    if not nome_montadora:
                        continue
                        
                    modelos_da_montadora = []
                    xpath_modelos_exato = "//div[contains(@class, 'automodel-menu-item')]//span[contains(@class, 'label')]"
                    
                    for tentativa_clique in range(2):
                        navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", montadora_atual)
                        time.sleep(0.5)
                        navegador.execute_script("arguments[0].click();", montadora_atual)
                        
                        time.sleep(0.8) 
                        
                        tentativas_espera = 0
                        while tentativas_espera < 20:
                            modelos_da_montadora = navegador.find_elements(By.XPATH, xpath_modelos_exato)
                            if len(modelos_da_montadora) > 0:
                                break 
                            
                            time.sleep(1)
                            tentativas_espera += 1
                            
                        if len(modelos_da_montadora) > 0:
                            break 
                        else:
                            if tentativa_clique == 0:
                                print(f"      [ALERTA] A montadora '{nome_montadora}' retornou 0. Reaplicando regra de 20s...")
                    
                    print(f"      -> {nome_montadora}: {len(modelos_da_montadora)} modelos salvos.")
                    
                    for modelo in modelos_da_montadora:
                        nome_modelo = modelo.text.strip()
                        if nome_modelo:
                            aba.append(['Motos', nome_manual, nome_submanual, nome_montadora, nome_modelo])

            if len(lista_submanuais) > 0:
                print(f"  Fechando a sanfona do manual '{nome_manual}'...")
                clicar_menu_exato(navegador, nome_manual)
                time.sleep(1)

        print("\nRASPAGEM DO PACOTE MOTOS CONCLUÍDA!")

    except Exception as e:
        print(f"Ocorreu um erro na extração do Motos: {e}")