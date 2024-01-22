import streamlit as st
from telegram import Bot, Update
from telegram.ext import CommandHandler, CallbackContext, Updater
import requests
import threading
import time

telegram_token = st.secrets['TOKEN']
url = "https://www.coingecko.com/price_charts/15269/usd/24_hours.json"

def scrape_valor(url):
             # Realizar la solicitud HTTP, simula un navegador....
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    data = response.json()
    valor = data["stats"][-1][-1]
    return valor


# Variables compartidas para almacenar el chat_id y el valor_objetivo
shared_chat_id = None
shared_valor_objetivo = None
shared_valor_actual = None
lock = threading.Lock()

# Función para realizar scraping y actualizar la variable compartida
def scrape_and_update_valor(url):
    global shared_valor_actual, app_running
    valor_actual = scrape_valor(url)
    with lock:
            shared_valor_actual = valor_actual
       

# Función para manejar el comando /start y obtener el chat_id y el valor objetivo
def start(update: Update, context: CallbackContext):
    global shared_chat_id
    chat_id = update.message.chat_id
    with lock:
        shared_chat_id = chat_id
    context.user_data['chat_id'] = chat_id
    update.message.reply_text("Ingresa tu valor objetivo en U$D. Ejemplo: '/objetivo 0.005'")

# Función para manejar el comando /objetivo y establecer valor_objetivo
def objetivo(update: Update, context: CallbackContext):
    global shared_valor_objetivo
    #chat_id = update.message.chat_id
    try:
        valor_objetivo = float(context.args[0])
        with lock:
            shared_valor_objetivo = valor_objetivo
        update.message.reply_text(f"¡Valor objetivo establecido en {valor_objetivo} U$D!")
    except (IndexError, ValueError):
        update.message.reply_text("Proporciona un valor válido. Ejemplo: '/objetivo 0.005'")

# Función para manejar el comando /stop y detener el bot
def stop(update: Update, context: CallbackContext):
    update.message.reply_text("Bot detenido.")
    updater.stop()
    context.job_queue.stop()
    context.user_data.clear()
    st_container.text("Bot detenido.")
    st.stop()

# Función para enviar alertas
def send_alert(chat_id, valor_objetivo, valor_actual):
    if chat_id is not None:
        if valor_objetivo is not None and valor_actual > valor_objetivo:
            mensaje = f"Nuevo precio UBI U$D: {round(valor_actual, 6)}"
            bot.send_message(chat_id=chat_id, text=mensaje)
            # Solicitar al usuario que ingrese un nuevo valor objetivo
            actualizar_valor_objetivo(chat_id, valor_objetivo)
                    
# Función para actualizar el valor objetivo
def actualizar_valor_objetivo(chat_id, valor_objetivo):
    nuevo_valor_objetivo = round(valor_objetivo * 1.05, 6)  # Incrementar en un 5%
    bot.send_message(chat_id=chat_id, text=f"Nuevo objetivo + 5%: {round(nuevo_valor_objetivo, 6)}")
    # Actualizar el valor objetivo compartido
    with lock:
        global shared_valor_objetivo
        shared_valor_objetivo = nuevo_valor_objetivo

# Configurar el bot con el token proporcionado por BotFather
bot = Bot(telegram_token)
updater = Updater(bot=bot, use_context=True)
dispatcher = updater.dispatcher

# Registrar el manejador para el comando /start y /objetivo
start_handler = CommandHandler('start', start)
objetivo_handler = CommandHandler('objetivo', objetivo)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(objetivo_handler)

# Registrar el manejador para el comando /stop
stop_handler = CommandHandler('stop', stop)
dispatcher.add_handler(stop_handler)

# Iniciar el bucle para recibir actualizaciones de Telegram en un hilo separado
updater_thread = threading.Thread(target=updater.start_polling)
updater_thread.start()

# Iniciar el scraping y la actualización del valor en un hilo separado
scrape_thread = threading.Thread(target=scrape_and_update_valor, args=(url,))
scrape_thread.start()

# Función para actualizar la interfaz y enviar alertas cada 10 segundos
def update_interface():
    global shared_chat_id, shared_valor_objetivo, shared_valor_actual
    with lock:
        chat_id = shared_chat_id
        valor_objetivo = shared_valor_objetivo
        valor_actual = shared_valor_actual

    st_container.markdown("[comandos del bot /start   /objetivo  /stop](https://t.me/Alert_1113311_bot)")


    if chat_id is not None:
        st_container.text(f'Precio actual UBI: {valor_actual:.6f}\n'
                          f'Valor objetivo recibido en la app: {valor_objetivo},\n')      
        # Pasa chat_id, valor_objetivo y valor_actual como argumentos
        send_alert(chat_id, valor_objetivo, valor_actual)
     
# Ejecutar la aplicación Streamlit
if __name__ == "__main__":
    st.title("Alerta Precio UBI")
    st_container = st.empty()  
    while True:
        update_interface()
        time.sleep(10)

    


    