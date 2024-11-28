from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import csv
import json

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
    
    # Trouver les blocs de produit
    product_blocks = soup.find_all("div", {"data-component-type": "s-search-result"})

    # Parcourir chaque bloc et extraire les données nécessaires
    products = []
    for product in product_blocks:
        if product:
            # Titre du produit
            title_element = product.find('h2')
            title = title_element.text.strip() if title_element else "Titre non trouvé"
            mark = title.split(" ")[0]

            if title =="Titre non trouvé":
                continue
            
            # Prix (si disponible)
            price_element = product.find('span', class_='a-price-whole')
            price = price_element.text.strip() if price_element else "Prix non trouvé"

            price_element2 = product.find("span", {"class": "a-price-fraction"})
            price2 = price_element2.text.strip() if price_element2 else "00"

            if price_element:
                full_price = f"{price}{price2}" if price != "Prix non disponible" else "Prix non disponible"
            else:
              
                # Chercher l'élément 'div' avec l'attribut 'data-cy' avant de tenter de chaîner d'autres méthodes
                secondary_offer = product.find('div', {"data-cy": "secondary-offer-recipe"})
                price_row = secondary_offer.find("div", class_="a-row a-size-base a-color-secondary") if secondary_offer else None

                # Extraire le prix ou retourner "tsisy" si non trouvé
                other_price = (price_row.find("span", class_="a-color-base").text.strip().replace('\xa0', ' ').split(" ")[0]
                    if price_row and price_row.find("span", class_="a-color-base") else "tsisy")
                full_price = other_price

                
                
            # Score du produit
            score_element = product.find('span', class_='a-icon-alt')
            score = score_element.text.strip().split(" ")[0] if score_element else "Score non trouvé"
                
            # Ajouter aux produits
            products.append({
                'mark': mark,
                'title': title,
                'price': convert_to_float(full_price),  # Convertir le prix en float
                'score': convert_to_float(score)  # Convertir le score en float
            })
    return products



# Fonction pour transformer en float
def convert_to_float(value):
    if value:
        # Remplacer la virgule par un point et tenter de convertir
        value = value.replace(',', '.').strip()
        try:
            return float(value)
        except ValueError:
            return 0.0  # Retourner 0.0 si la conversion échoue
    return 0.0  # Retourner 0.0 si la valeur est vide


# Fonction pour enregistrer les résultats dans un fichier CSV
def save_to_csv(products):
    # Liste des noms de colonnes, incluez toutes les clés possibles
    fieldnames = ['title', 'price', 'mark', 'score']

    # Ouvrir un fichier CSV en mode écriture
    with open('products.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Écrire l'en-tête
        writer.writeheader()

        # Écrire les données
        for product in products:
            # Compléter les valeurs manquantes
            product = {key: product.get(key, 'Donnée manquante') for key in fieldnames}
            writer.writerow(product)


def pagination():
    store = []  # Liste pour stocker tous les produits récupérés
    
    for iteration in range(1, 8):  # Boucler sur les pages de 1 à 8
        url = f"https://www.amazon.fr/s?k=telephone+portable&page={iteration}&crid=QYI5TVHCWQ8Z&qid=1732778348&sprefix=te%2Caps%2C723&ref=sr_pg_{iteration}"
        result = getInfo(url)  # Récupérer les informations de la page
        store.extend(result)  # Ajouter les produits récupérés à la liste
    
    return store



# Fonction pour enregistrer les résultats dans un fichier JSON
def save_to_json(products):
    # Spécifier le nom du fichier JSON
    filename = 'products.json'

    # Ouvrir le fichier en mode écriture
    with open(filename, mode='w', encoding='utf-8') as file:
        # Compléter les valeurs manquantes et écrire les données dans le fichier JSON
        for product in products:
            # Compléter les valeurs manquantes
            product = {key: product.get(key, 'Donnée manquante') for key in ['title', 'price', 'mark', 'score']}
        
        # Enregistrer les données dans le fichier JSON
        json.dump(products, file, ensure_ascii=False, indent=4)


def scrapper():
    # Récupérer tous les produits à partir des pages
    all_products = pagination()

    # Enregistrer les résultats dans un fichier CSV
    save_to_csv(all_products)

    save_to_json(all_products)

    # Affichage des résultats dans la console
    for product in all_products:
        print(product)


# Exemple d'utilisation
if __name__ == "__main__":    
    scrapper()



