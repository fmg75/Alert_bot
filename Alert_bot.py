import streamlit as st
from telegram import Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.utils.request import Request
import requests
from lxml import html
import time

# Definir valores fijos (token y chat_id)
url = 'https://www.coingecko.com/es/monedas/universal-basic-income'
telegram_token = '6529284879:AAGnwzxSS2DauwYdsEEyMvI__ZelSbfchTg'

alerta_enviada = False

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
            time.sleep(5)  # Esperar 5 segundos antes de intentar nuevamente


def enviar_alerta_telegram(token, chat_id, mensaje):
    bot = Bot(token)
    bot.send_message(chat_id=chat_id, text=mensaje)

def start(update: Updater, context: CallbackContext) -> None:
    global chat_id
    chat_id = update.message.chat_id
    context.user_data['chat_id'] = chat_id
    update.message.reply_text(f"Tu chat_id es : {chat_id}")

def main():
    global alerta_enviada  # Declarar como global
    st.title("Alerta UBI")

# Mostrar un mensaje de instrucciones
#st.write("Haz clic en el siguiente enlace para iniciar una conversación con el bot de Telegram:")
    st.markdown("[Iniciar conversación con el bot de Telegram](https://t.me/fer_alert_bot)")

    # Campo para ingresar el chat_id
    chat_id = st.text_input("Ingresa tu chat_id (iniciar en chatbot con /start) ")

# Verificar si se ingresó un chat_id y mostrar el campo Alerta cuando supere:
    if chat_id:
        valor_inicial = scrape_valor(url)

        # Campo para ingresar el valor objetivo
        valor_objetivo = st.number_input("Alerta cuando supere: ", value=round(1.001 * float(valor_inicial), 8), format="%.8f", step=0.1 * float(valor_inicial))

        while True:
        # Llamar a la función de scrape con la URL proporcionada
            valor_actual = scrape_valor(url)
        
            if valor_actual > valor_objetivo and not alerta_enviada:
            # Enviar alerta a Telegram
                mensaje = f"Nuevo valor UBI U$D: {valor_actual}"
                enviar_alerta_telegram(telegram_token, chat_id, mensaje)
                alerta_enviada = False
        
            time.sleep(30)

def configurar_telegram():
    request = Request(con_pool_size=8)
    bot = Bot(token=telegram_token, request=request)
    updater = Updater(bot=bot, use_context=True)
    
    try:
        updater.bot.setWebhook(url='https://alertubi.streamlit.app/')
    except Exception as e:
        error_message = str(e)
        if 'RetryAfter' in error_message:
            retry_after_index = error_message.find('RetryAfter')
            retry_after_value = float(error_message[retry_after_index:].split()[1])
            print(f"Se excedió el límite de envío. Esperando {retry_after_value} segundos antes de intentar nuevamente.")
            time.sleep(retry_after_value)
            updater.bot.setWebhook(url='https://alertubi.streamlit.app/')
        else:
            print(f"Error al establecer el webhook: {e}")

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    
if __name__ == "__main__":
    configurar_telegram()
    main()
