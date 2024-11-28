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
    cards = soup.find_all('div', class_="product-tile-wrapper")
    for card in cards:
        cardtitle = card.find("div", class_="tile-body")
        category = cardtitle.find('p', class_="flap text-functional-1").get_text(strip=True)
        nom_produit = cardtitle.find("a", class_="link text-primary-3").get_text(strip=True)
        price = cardtitle.find("div", class_="mpx-promo-container tile-promo").find("span", class_="sales").find("span", class_="value").get_text(strip=True)
        
        product_info = {
            "category": category,
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
        c.drawString(50, y, f"Catégorie : {product['category']}")
        y -= 15
        c.drawString(50, y, f"Nom : {product['nom_produit']}")
        y -= 15
        c.drawString(50, y, f"Prix : {product['price']}")
        y -= 25  # Espace entre les produits
    
    c.save()
    print(f"PDF généré : {file_name}")

def scrapper():
    # Récupérer les informations et générer le PDF
    # start=200
    # iteration=200
    all_products = getInfo(f"https://www.monoprix.fr/c/mode/femme")
    export_to_pdf(all_products)

# Exemple d'utilisation
if __name__ == "__main__":    
    scrapper()
