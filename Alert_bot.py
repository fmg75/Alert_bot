import streamlit as st
import requests
import time
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from lxml import html
#import config
import os
import sys

# Redirigir la salida estándar y de error a os.devnull 
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

# URL de scraping
url = 'https://www.coingecko.com/es/monedas/universal-basic-income'
#telegram_token = config.TOKEN
telegram_token = st.secrets["TOKEN"]

# Función para realizar el scraping de valor
def scrape_valor(url):
    while True:
        try:
            # Realizar la solicitud HTTP, simula un navegador....
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = requests.get(url, headers=headers)

            tree = html.fromstring(response.content)
            # Utilizar XPath para encontrar el elemento span específico
            xpath = '/html/body/div[3]/main/div[1]/div[1]/div/div[1]/div[2]/div/div[1]/span[1]/span'
            valor_element = tree.xpath(xpath)

            # Verificar si valor_element está vacío
            if not valor_element:
                raise ValueError("No se pudo encontrar el elemento span específico")

            # Extraer el contenido del elemento en formato adecuado
            valor = valor_element[0].text_content().strip()
            return float(valor.replace('$', '').replace(',', '.'))
        except Exception as e:
            print(f"Error al obtener el valor: {e}")
            time.sleep(1)

# Función para enviar alerta a Telegram
def enviar_alerta_telegram(token, chat_id, mensaje):
    bot = Bot(token)
    bot.send_message(chat_id=chat_id, text=mensaje)

# Función para manejar el comando /start
def start(update, context):
    chat_id = update.message.chat_id
    context.user_data['chat_id'] = chat_id
    update.message.reply_text(f"Tu chat_id es: {chat_id}")

# Función principal para configurar el bot de Telegram
def telegram_bot():
    bot = Bot(token=telegram_token)
    updater = Updater(bot=bot, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()

# Función principal para la interfaz de Streamlit
def interface():
    st.title("Alerta UBI")
    st.markdown("[Iniciar conversación con el bot de Telegram](https://t.me/Alert_7011371_bot)")
    
    # Campo para ingresar el chat_id
    chat_id = st.text_input("Ingresa tu chat_id (iniciar en chatbot con /start) ")

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

        #valor_actual = scrape_valor(url)
        #st.write('Valor actual ', valor_actual)

    while True:
        st.session_state.valor_objetivo = valor_objetivo
        valor_actual = scrape_valor(url)

        if valor_actual > valor_objetivo:
            mensaje = f"Nuevo valor UBI U$D: {valor_actual}"
            enviar_alerta_telegram(telegram_token, chat_id, mensaje)
            break
        

if __name__ == "__main__":

    telegram_bot()
    interface()
    

    