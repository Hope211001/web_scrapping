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
    
    products = []
    cards = soup.find_all("li", class_="ajax_block_product")
    for card in cards:
        parent1 = card.find()
        parent = card.find("div", class_="product-container")
        card_title = parent.find("div", class_="right-block")
        nom_produit = card_title.find("h5").find("a", class_="product-name").find("span", class_="grid-name").get_text(strip=True)
        price = card_title.find("div", class_="content_price").find("span", class_="price product-price").get_text(strip=True)
        
        product_info = {
            "nom_produit": nom_produit,
            "price": price
        }
        products.append(product_info)
    
    return products

# Fonction pour écrire les informations dans un PDF
def export_to_pdf(data):

   
    file_name=f"pdf/file-{uuid.uuid4()}.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter
    y = height - 50  # Position initiale
    
    c.setFont("Helvetica", 12)
    c.drawString(50, y, "Liste des Produits :")
    y -= 20

    for product in data:
        if y < 50:  # Si l'espace est insuffisant, créer une nouvelle page
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 50
        y -= 15
        c.drawString(50, y, f"Nom : {product['nom_produit']}")
        y -= 15
        c.drawString(50, y, f"Prix : {product['price']}")
        y -= 25  # Espace entre les produits
    
    c.save()
    print(f"PDF généré : {file_name}")

def scrapper():
    # Récupérer les informations et générer le PDF
    store = []  # Initialiser une liste pour stocker tous les produits
    
    for iteration in range(1, 9):  # Boucler sur les pages de 1 à 8
        all_products = getInfo(f"https://www.hoptoys.fr/lexique-imagerie-langage-oral-c-933.html?p={iteration}")
        store.extend(all_products)  # Ajouter les produits récupérés à la liste
    
    # Exporter les données dans un PDF
    export_to_pdf(store)

# Exemple d'utilisation
if __name__ == "__main__":    
    scrapper()
