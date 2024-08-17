import requests
from bs4 import BeautifulSoup

# URL de la página
url = "https://www.cepal.org/es"

# Realiza la solicitud HTTP a la página
response = requests.get(url)

# Analiza el contenido HTML de la página
soup = BeautifulSoup(response.text, "html.parser")

# Busca todas las ocurrencias de la palabra "México"
resultados = soup.find_all(string=lambda text: "Igualdad" in text)

# Imprime las ocurrencias encontradas
for resultado in resultados:
    print(resultado)