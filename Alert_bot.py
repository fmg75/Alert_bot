import streamlit as st
import requests
from datetime import datetime, timedelta
import time
from telegram import Bot
#import config

# URL de scraping
url = "https://www.coingecko.com/price_charts/15269/usd/24_hours.json"
#telegram_token = config.TOKEN
telegram_token = st.secrets["TOKEN"]

def scrape_valor(url):
             # Realizar la solicitud HTTP, simula un navegador....
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    data = response.json()

            # Extrae hora
    timestamp_milliseconds = data["stats"][-1][0]
    timestamp_seconds = timestamp_milliseconds / 1000
    datetime_object_utc = datetime.utcfromtimestamp(timestamp_seconds)
    # Ajustar a la zona horaria restando 2 horas
    datetime_object_local = datetime_object_utc - timedelta(hours=3)
    
    # Formatear la fecha y hora como hh:mm:ss
    formatted_time = datetime_object_local.strftime("%H:%M:%S")
    rounded_seconds = round(datetime_object_local.second)

    last_element = data["stats"][-1][-1]
    
    return last_element,formatted_time,rounded_seconds
       
# Función para enviar alerta a Telegram
def enviar_alerta_telegram(token, chat_id, mensaje):
    bot = Bot(token)
    bot.send_message(chat_id=chat_id, text=mensaje)


#interfaz de Streamlit
st.title("Alerta UBI")
st.markdown("[Envia 'Hola' al bot de Telegram](https://t.me/Alert_7011371_bot)")

def chat():

    response = requests.get(f'https://api.telegram.org/bot{telegram_token}/getUpdates')

    updates = response.json().get('result', [])

    for update in updates:
        message = update.get('message', {})
        text = message.get('text', '')

        # Verificar si el mensaje contiene 'hola'
        if 'Hola' in text:

        # Obtener el chat_id del usuario que envió el mensaje
            chat_id = message['chat']['id']
            return chat_id


valor_objetivo = st.number_input(
            "Alerta cuando el precio supere: ",
            value=0.001,
            format="%.6f",
            step=0.00005
        )
    
# Crear un contenedor para mostrar el valor
container = st.empty()

while True:
    valor_actual, formatted_time, rounded_seconds = scrape_valor(url)

    # Concatena el valor actual y la leyenda del dato del tiempo en el contenedor
    texto_mostrado = 'Precio actual UBI: {:.6f}    Ultima actualizacion precio: {}'.format(valor_actual, formatted_time[:-2] + f"{rounded_seconds:02}")
    container.text(texto_mostrado)
    
    if valor_actual > valor_objetivo:
        mensaje = f"Nuevo precio UBI U$D: {round(valor_actual,6)}"
        chat_id = chat()
        if chat_id:
            enviar_alerta_telegram(telegram_token, chat_id, mensaje)
        else:
            container.text('Saluda al bot para recibir notificaciones!')
            time.sleep(5)
        break

    time.sleep(60)