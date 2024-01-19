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
    while True:
            # Realizar la solicitud HTTP, simula un navegador....
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = requests.get(url, headers=headers)

            tree = html.fromstring(response.content)
            # Utilizar XPath para encontrar el elemento span específico
            xpath = '/html/body/div[3]/main/div[1]/div[1]/div/div[1]/div[2]/div/div[1]/span[1]/span'
            valor_element = tree.xpath(xpath)
            valor = valor_element[0].text_content().strip()
            return float(valor.replace('$', '').replace(',', '.'))
       
# Función para enviar alerta a Telegram
def enviar_alerta_telegram(token, chat_id, mensaje):
    bot = Bot(token)
    bot.send_message(chat_id=chat_id, text=mensaje)


#interfaz de Streamlit
st.title("Alerta UBI")
st.markdown("[Iniciar conversación con el bot de Telegram](https://t.me/Alert_7011371_bot)")

response = requests.get(f'https://api.telegram.org/bot{telegram_token}/getUpdates')

chat_id = response.json()['result'][0]['message']['chat']['id']
valor_objetivo = st.number_input(
            "Alerta cuando supere: ",
            value=0.001,
            format="%.8f",
            step=0.00005
        )
    
# Crear un contenedor para mostrar el valor
container = st.empty()

while True:
    valor_actual = scrape_valor(url)
    container.text('Valor actual UBI: {:.8f}'.format(valor_actual))  # Muestra el valor en una sola línea

    if valor_actual > valor_objetivo:
        mensaje = f"Nuevo valor UBI U$D: {valor_actual}"
        enviar_alerta_telegram(telegram_token, chat_id, mensaje)
        break

    time.sleep(3)