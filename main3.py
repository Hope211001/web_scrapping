from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import time
import uuid

# Utiliser webdriver-manager pour obtenir le bon ChromeDriver
driver_path = ChromeDriverManager().install()

# Créer un objet Service pour spécifier le chemin de ChromeDriver
service = Service(executable_path=driver_path)

# Initialiser le WebDriver avec l'objet Service
driver = webdriver.Chrome(service=service)



# Fonction pour extraire les informations d'une URL
def getInfo(url):
    print(url)
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    product_list = []
  # Chercher tous les blocs qui semblent contenir des produits
    for product in soup.find_all(lambda tag: tag.name == "div" and len(tag.find_all()) > 2):
        # Trouver le nom (heuristique : balises avec texte descriptif)
        name_tag = product.find(lambda tag: tag.name in ["h1", "h2", "h3", "p", "a"] and len(tag.text.strip()) > 2)
        name = name_tag.text.strip() if name_tag else "Non trouvé"

        # Trouver le prix (heuristique : texte avec symboles monétaires)
        price_tag = product.find(string=lambda text: text and ("€" in text or "$" in text))
        price = price_tag.strip() if price_tag else "Non trouvé"

        # Ajouter le produit si nom ou prix trouvé
        if name != "Non trouvé" or price != "Non trouvé":
            product_list.append({ "name": name, "price": price})

    print(product_list)
    return product_list
   
# Exemple d'utilisation
if __name__ == "__main__":
    getInfo(f"https://www.hoptoys.fr/perception-visuelle-et-auditive-c-3150.html")
