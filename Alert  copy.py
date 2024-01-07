import requests
from lxml import html

def scrape_valor(url):
    # Realizar la solicitud HTTP, simula un navegador....
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Parsear el contenido HTML de la página utilizando lxml
        tree = html.fromstring(response.content)

        # Utilizar XPath para encontrar el elemento span específico
        xpath = '//*[@id="price"]/div/div[1]/div[1]/span/span/span[2]'
        valor_element = tree.xpath(xpath)

        # Verificar si se encontró el elemento
        if valor_element:
            # Extraer el contenido del elemento
            valor = valor_element[0].text_content().strip()
            return valor
        else:
            print("No se encontró el elemento con XPath especificado.")
            return None
    else:
        print(f"Error al obtener la página. Código de estado: {response.status_code}")
        return None

# URL de la página web que deseas scrapear
url = 'https://articulo.mercadolibre.com.ar/MLA-909556758-chomba-de-hombre-montagne-dry-pro-_JM#reco_item_pos=1&reco_backend=item_decorator&reco_backend_type=function&reco_client=home_items-decorator-legacy&reco_id=98dac2db-e255-4257-b647-cffadc875911&c_id=/home/bookmarks-recommendations-seed/element&c_uid=231f971d-d8b4-425b-aaf3-3eb69654ef0c&da_id=bookmark&da_position=1&id_origin=/home/dynamic_access&da_sort_algorithm=ranker'

# Llamar a la función de scrape con la URL proporcionada
resultado = scrape_valor(url)

# Imprimir el resultado
if resultado:
    print(f"El valor extraído es: {resultado}")


