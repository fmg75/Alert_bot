import requests
import asyncio
from lxml import html
from telegram import Bot
from telegram.constants import ParseMode

async def scrape_valor(url):
    # Realizar la solicitud HTTP, simula un navegador....
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Parsear el contenido HTML de la página utilizando lxml
        tree = html.fromstring(response.content)

        # Utilizar XPath para encontrar el elemento span específico
        xpath_expression = '/html/body/div[3]/main/div[1]/div[1]/div/div[1]/div[2]/div/div[1]/span[1]/span'
        valor_element = tree.xpath(xpath_expression)

        # Extraer el contenido del elemento (sin verificar si se encontró o no)
        valor = valor_element[0].text_content().strip()
        return valor
    else:
        print(f"Error al obtener la página. Código de estado: {response.status_code}")
        return None

async def enviar_alerta_telegram(token, chat_id, mensaje):
    bot = Bot(token)
    await bot.send_message(chat_id=chat_id, text=mensaje, parse_mode=ParseMode.MARKDOWN)

async def main():
    # URL de la página web que deseas scrapear
    url = 'https://www.coingecko.com/es/monedas/universal-basic-income'

    # Token y Chat ID de tu bot de Telegram
    telegram_token = '6529284879:AAGnwzxSS2DauwYdsEEyMvI__ZelSbfchTg'
    chat_id = '1560847300'  # Reemplaza con el valor correcto

    # Llamar a la función de scrape con la URL proporcionada
    resultado = await scrape_valor(url)

    # Imprimir el resultado
    if resultado:
        mensaje = f"El valor extraído es: ${resultado}"

        # Enviar alerta a Telegram
        await enviar_alerta_telegram(telegram_token, chat_id, mensaje)

if __name__ == "__main__":
    # Ejecutar el bucle de eventos de asyncio
    asyncio.run(main())

