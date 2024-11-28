from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import csv

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
    
    products = []

    # Cherche tous les conteneurs de produit (ici, identifiés par `s-result-item`)
    results = soup.find_all("div", {"data-component-type": "s-search-result"})

    # Parcours des résultats pour extraire des détails spécifiques
    for result in results:
        # Extraire le titre du produit
        title = result.find("span", {"class": "a-size-medium"})
        title = title.text.strip() if title else "Titre non disponible"
        
         # Prix
        price = result.find("span", {"class": "a-price-whole"})
        price = price.text.strip() if price else "Prix non disponible"
        
        price2 = result.find("span", {"class": "a-price-fraction"})
        price2 = price2.text.strip() if price2 else "00"

        other_price = result.find('span', {'class': 'a-color-base'})
        other_price = other_price.text.strip() if other_price else "Prix non disponible"

        # Vérifier si le prix est vide, et si c'est le cas, utiliser le prix alternatif
        if price == "":  
            full_price = other_price
        else:
            full_price = f"{price}{price2}" if price != "Prix non disponible" else "Prix non disponible"
        
        # Extraire les avis clients (si disponible)
        rating = result.find("span", {"class": "a-icon-alt"})
        rating = rating.text.strip() if rating else "Pas de notes disponibles"

        product_info = {
                "title" : title,
                "prix" : full_price,
                "score" : rating,
        }
        products.append(product_info)

    print(len(products))
    return products

# Fonction pour enregistrer les résultats dans un fichier CSV
def save_to_csv(products, filename="products.csv"):
    # Ouvrir le fichier CSV en mode écriture
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["title", "prix", "score"])
        
        # Écrire l'en-tête (noms des colonnes)
        writer.writeheader()
        
        # Écrire les informations des produits
        for product in products:
            writer.writerow(product)

def pagination():
    store = []  # Liste pour stocker tous les produits récupérés
    
    for iteration in range(1, 3):  # Boucler sur les pages de 1 à 8
        url = f"https://www.amazon.fr/s?k=telephone+portable&i=electronics&rh=n%3A13921051%2Cp_123%3A46655&dc&page={iteration}&crid=2228HR3IU9F78&qid=1732713901&rnid=91049112031&sprefix=te%2Caps%2C462&ref=sr_pg_{iteration}"                                                                                                                                                                                                                  

        result = getInfo(url)  # Récupérer les informations de la page
        store.extend(result)  # Ajouter les produits récupérés à la liste
    
    return store

# Récupérer tous les produits à partir des pages
all_products = pagination()

# Enregistrer les résultats dans un fichier CSV
save_to_csv(all_products)

# Affichage des résultats dans la console
for product in all_products:
    print(product)






