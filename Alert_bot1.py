import streamlit as st
from telegram import Bot
from telegram.constants import ParseMode
import requests
from lxml import html
import asyncio

# Definir valores fijos (token y chat_id)
url = 'https://etherscan.io/dex/uniswapv2/0xe632ded5195e945a31f56d674aab0c0c9e7e812c'
telegram_token = '6529284879:AAGnwzxSS2DauwYdsEEyMvI__ZelSbfchTg'
chat_id = '1560847300'

alerta_enviada = False

st.title("Alerta UBI")

async def scrape_valor(url):
    # Realizar la solicitud HTTP, simula un navegador....
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    tree = html.fromstring(response.content)

    # Utilizar XPath para encontrar el elemento span específico 
    
    xpath = '/html/body/main/section[2]/div[2]/div[1]/div/div[1]/div/div[1]/span'
    valor_element = tree.xpath(xpath)

    # Extraer el contenido del elemento en formato adecuado
    valor = valor_element[0].text_content().strip()
    return float(valor.replace('$', ''))

async def enviar_alerta_telegram(token, chat_id, mensaje):
    bot = Bot(token)
    await bot.send_message(chat_id=chat_id, text=mensaje, parse_mode=ParseMode.MARKDOWN)

async def main():
    global valor_objetivo, alerta_enviada
    
    # Obtener el valor inicial para el campo objetivo + 10%
    valor_inicial = await scrape_valor(url)
    valor_objetivo = st.number_input("Alerta cuando supere :", value=round(1.001 * float(valor_inicial), 8), format="%.8f",step = 0.1 * float(valor_inicial))
    
    # Actualizar la variable global al ingresar un nuevo valor objetivo
    if valor_objetivo != float(valor_inicial):
        alerta_enviada = False

    # Agregar el enlace al bot de Telegram
    st.markdown("[Accede al bot de Telegram](https://t.me/fer_alert_bot)")

    while True:
        # Llamar a la función de scrape con la URL proporcionada
        valor_actual = await scrape_valor(url)
        
        mensaje = f"Nuevo valor UBI U$D: {valor_actual}"

        if valor_actual > valor_objetivo and not alerta_enviada:
            # Enviar alerta a Telegram
            await enviar_alerta_telegram(telegram_token, chat_id, mensaje)
            alerta_enviada = True
        
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
