import time
from selenium.webdriver.common.by import By

def clicar_menu_exato(navegador, nome_item, tempo_maximo=10):
    """
    Procura e clica exatamente no item do menu informado.
    """

    tempo_inicial = time.time()

    while time.time() - tempo_inicial < tempo_maximo:

        try:
            labels = navegador.find_elements(
                By.XPATH,
                "//aside[1]//span[contains(@class, 'label')]"
            )

            for label in labels:

                texto_label = (
                    label.get_attribute("textContent")
                    .strip()
                    .upper()
                )

                texto_buscado = nome_item.strip().upper()

                if texto_label == texto_buscado:

                    navegador.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'});",
                        label
                    )

                    time.sleep(0.8)

                    navegador.execute_script(
                        "arguments[0].click();",
                        label
                    )

                    return True

        except Exception as e:
            print(f"[UTILS] Erro ao clicar menu: {e}")

        time.sleep(1)

    return False