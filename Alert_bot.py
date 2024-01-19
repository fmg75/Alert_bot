import streamlit as st
import requests
import time
from telegram import Bot
from lxml import html
#import config

# URL de scraping
url = 'https://www.coingecko.com/es/monedas/universal-basic-income'
#telegram_token = config.TOKEN
telegram_token = st.secrets["TOKEN"]

def scrape_valor(url):
            # Realizar la solicitud HTTP, simula un navegador....
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = requests.get(url, headers=headers)
            tree = html.fromstring(response.content)
            # Utilizar XPath para encontrar el elemento span específico
            xpath = '/html/body/div[3]/main/div[1]/div[1]/div/div[1]/div[2]/div/div[1]/span[1]/span'
            valor_element = tree.xpath(xpath)
            # Extraer el contenido del elemento en formato adecuado
            valor = valor_element[0].text_content().strip()
            return float(valor.replace('$', '').replace(',', '.'))
        
# Función para enviar alerta a Telegram
def enviar_alerta_telegram(token, chat_id, mensaje):
    bot = Bot(token)
    bot.send_message(chat_id=chat_id, text=mensaje)

# Función principal para la interfaz de Streamlit
def interface():
    st.title("Alerta UBI")
    st.markdown("[Iniciar conversación con el bot de Telegram](https://t.me/Alert_7011371_bot)")
    
    response = requests.get(f'https://api.telegram.org/bot{telegram_token}/getUpdates')
    chat_id = response.json()['result'][0]['message']['chat']['id']

    # Inicializar valor_objetivo fuera de la condición
    valor_objetivo = st.session_state.get('valor_objetivo', 0.00100000)
    valor_actual = scrape_valor(url)
    st.write('Valor actual UBI', valor_actual)

    # Verificar si se ingresó un chat_id y mostrar el campo Alerta cuando supere
    if chat_id:
        input_key = "valor_objetivo_input"
        valor_objetivo = st.number_input(
            "Alerta cuando supere: ",
            value=valor_objetivo,
            format="%.8f",
            step=0.00005,
            key=input_key
        )

    while True:
        
        st.session_state.valor_objetivo = valor_objetivo
        valor_actual = scrape_valor(url)

        if valor_actual > valor_objetivo:
            mensaje = f"Nuevo valor UBI U$D: {valor_actual}"
            enviar_alerta_telegram(telegram_token, chat_id, mensaje)
            time.sleep(10)
        

if __name__ == "__main__":
     interface()

    

    