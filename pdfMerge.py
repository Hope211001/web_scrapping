from PyPDF2 import PdfMerger
import os

def recuperer_pdfs(dossier):
    """
    Récupère tous les fichiers PDF dans un dossier donné.

    Args:
        dossier (str): Chemin du dossier à analyser.

    Returns:
        list: Liste des chemins des fichiers PDF trouvés.
    """
    pdfs = []
    try:
        # Parcourir tous les fichiers dans le dossier
        for fichier in os.listdir(dossier):
            # Construire le chemin complet
            chemin_complet = os.path.join(dossier, fichier)
            # Vérifier si c'est un fichier PDF
            if os.path.isfile(chemin_complet) and fichier.lower().endswith('.pdf'):
                pdfs.append(chemin_complet)
    except FileNotFoundError:
        print(f"Le dossier '{dossier}' n'existe pas.")
    except PermissionError:
        print(f"Permission refusée pour accéder au dossier '{dossier}'.")
    
    return pdfs



def combine_pdfs():
    filename=input("entrer le nom du pdf final que vous voulez? ")
    output_file=f"{filename}.pdf"
    pdf_list=recuperer_pdfs("pdf")
    """
    Combine plusieurs fichiers PDF en un seul fichier.
    Args:
        pdf_list (list): Liste des chemins des fichiers PDF à combiner.
        output_file (str): Chemin du fichier PDF de sortie.
    Returns:
        None
    """
    merger = PdfMerger()

    try:
        # Parcourir chaque fichier PDF et les ajouter au merger
        for pdf in pdf_list:
            print(f"Ajout de {pdf}...")
            merger.append(pdf)
        
        # Écrire le fichier combiné
        merger.write(output_file)
        print(f"PDF combiné créé : {output_file}")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    finally:
        merger.close()

# Exemple d'utilisation
if __name__ == "__main__":    
    combine_pdfs()
