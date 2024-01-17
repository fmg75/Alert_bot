import streamlit as st
from telegram import Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
from lxml import html
import time

# Definir valores fijos (token y chat_id)
url = 'https://www.coingecko.com/es/monedas/universal-basic-income'
telegram_token = '6529284879:AAGnwzxSS2DauwYdsEEyMvI__ZelSbfchTg'

alerta_enviada = False

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

def enviar_alerta_telegram(token, chat_id, mensaje):
    bot = Bot(token)
    bot.send_message(chat_id=chat_id, text=mensaje)

def start(update: Updater, context: CallbackContext) -> None:
    global chat_id
    chat_id = update.message.chat_id
    context.user_data['chat_id'] = chat_id
    update.message.reply_text(f"¡Hola! Tu chat_id es {chat_id}")

def main():
    global alerta_enviada  # Declarar como global
    st.title("Alerta UBI")

# Mostrar un mensaje de instrucciones
#st.write("Haz clic en el siguiente enlace para iniciar una conversación con el bot de Telegram:")
    st.markdown("[Iniciar conversación con el bot de Telegram](https://t.me/fer_alert_bot)")

    # Campo para ingresar el chat_id
    chat_id = st.text_input("Ingresa tu chat_id (obtenido al iniciar la conversación con el bot de Telegram):")

# Verificar si se ingresó un chat_id y mostrar el campo Alerta cuando supere:
    if chat_id:
        valor_inicial = scrape_valor(url)

        # Campo para ingresar el valor objetivo
        valor_objetivo = st.number_input("Alerta cuando supere:", value=round(1.001 * float(valor_inicial), 8), format="%.8f", step=0.1 * float(valor_inicial))

        while True:
        # Llamar a la función de scrape con la URL proporcionada
            valor_actual = scrape_valor(url)
        
            mensaje = f"Nuevo valor UBI U$D: {valor_actual}"

            if valor_actual > valor_objetivo and not alerta_enviada:
            # Enviar alerta a Telegram
                enviar_alerta_telegram(telegram_token, chat_id, mensaje)
                alerta_enviada = True
        
            time.sleep(30)


def configurar_telegram():
    bot = Bot(token=telegram_token)
    updater = Updater(bot=bot, use_context=True)
    updater.bot.setWebhook()
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()

if __name__ == "__main__":
    configurar_telegram()
    main()
