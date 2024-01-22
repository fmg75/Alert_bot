import requests
import config

def detener_bot(token):
    url = f"https://api.telegram.org/bot{token}/close"

    try:
        response = requests.post(url)
        response.raise_for_status()
        print("Instancia del bot detenida exitosamente.")
        print(response)
    except requests.exceptions.RequestException as e:
        print(f"Error al detener la instancia del bot: {e}")

# Reemplaza 'TU_TOKEN' con el token real de tu bot.
token = config.TOKEN
detener_bot(token)
