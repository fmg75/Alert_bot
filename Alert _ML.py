import requests
from lxml import html

def scrape_valor(url):
    # Realizar la solicitud HTTP, simula un navegador....
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    tree = html.fromstring(response.content)

    # Utilizar XPath para encontrar el elemento span específico
    xpath = '//*[@id="price"]/div/div[1]/div[1]/span/span/span[2]'
    valor_element = tree.xpath(xpath)

    return valor_element[0].text_content().strip()
  
# URL de la página web que deseas scrapear
url = 'https://articulo.mercadolibre.com.ar/MLA-881360235-chomba-secado-rapido-dry-pro-hombre-montagne-verano-fresca-_JM#polycard_client=recommendations_home_navigation-recommendations&reco_backend=machinalis-homes-univb&reco_client=home_navigation-recommendations&reco_item_pos=2&reco_backend_type=function&reco_id=138c9af5-4a3c-41bb-9807-8057588f2f43&c_id=/home/navigation-recommendations/element&c_uid=e3501d1d-b391-4290-8100-82976d216b1a'

# Llamar a la función de scrape con la URL proporcionada
resultado = scrape_valor(url)


print(f"El valor extraído es: {resultado}")


