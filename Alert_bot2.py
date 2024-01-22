
import streamlit as st
from telegram import Bot, Update
from telegram.ext import CommandHandler, CallbackContext, Updater
import config
import time
from datetime import datetime, timedelta
import requests

telegram_token = config.TOKEN
url = "https://www.coingecko.com/price_charts/15269/usd/24_hours.json"

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

# Variable global para almacenar el chat_id
chat_id = None

# Función para manejar el comando /start y obtener el chat_id y valor_objetivo
def start(update: Update, context: CallbackContext):
    global chat_id, valor_objetivo
    chat_id = update.message.chat_id
    context.user_data['chat_id'] = chat_id
    update.message.reply_text(f"¡Hola! Tu chat_id es {chat_id}")

# Configurar el bot con el token proporcionado por BotFather
bot = Bot(telegram_token)
updater = Updater(bot=bot, use_context=True)
dispatcher = updater.dispatcher

# Registrar el manejador para el comando /start y obtiene chat_id solo si aún no se ha obtenido
if chat_id is None:
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    # Iniciar el bucle para recibir actualizaciones y obtener el chat_id
    updater.start_polling()

# Interfaz de Streamlit
st.title("Alerta UBI")
st.markdown("[Envía '/start' al bot de Telegram](https://t.me/Alert_7011371_bot), ¡Esperando!")

# Esperar a que el usuario interactúe con el bot y obtenga el chat_id
while chat_id is None:
    time.sleep(1)

# Detener la recepción de actualizaciones después de obtener el chat_id
updater.stop()

# Mostrar la interfaz para ingresar el valor objetivo
st.empty()  # Limpiar la interfaz después de obtener el chat_id
valor_objetivo = st.number_input("Alerta cuando el precio supere: ", value=0.001, format="%.6f", step=0.00005)


def send_alert():
    valor_actual, formatted_time, rounded_seconds = scrape_valor(url)
    #st.text(texto_mostrado)
    if valor_actual>valor_objetivo:
        mensaje = f"Nuevo precio UBI U$D: {round(valor_actual, 6)}"
        bot.send_message(chat_id=chat_id, text=mensaje)

# Tarea programada para verificar el precio cada 10 segundos
conteiner = st.empty()
while True:
    time.sleep(3)
    valor_actual, formatted_time, rounded_seconds = scrape_valor(url)
    # Concatena el valor actual y la leyenda del dato del tiempo en el contenedor
    conteiner.text('Precio actual UBI: {:.6f}    Ultima actualizacion precio: {}'.format(valor_actual, formatted_time[:-2] + f"{rounded_seconds:02}"))
    send_alert()
