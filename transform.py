import markdown
import os

def convert_md_to_html(md_file_path):
    # Vérifie si le fichier MD existe
    if not os.path.exists(md_file_path):
        print(f"Le fichier {md_file_path} n'existe pas.")
        return

    # Récupère le contenu du fichier MD
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()

    # Convertit le contenu Markdown en HTML
    html_content = markdown.markdown(md_content)

    # Crée le chemin du fichier HTML dans le même répertoire que le fichier MD
    html_file_path = os.path.splitext(md_file_path)[0] + '.html'

    # Écrit le contenu HTML dans le fichier
    with open(html_file_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

    print(f"Conversion réussie. Le fichier HTML a été créé : {html_file_path}")

if __name__ == "__main__":
    # Demande à l'utilisateur de saisir le chemin du fichier MD
    md_file_path = input("Entrez le chemin du fichier MD : ").strip()

    # Appelle la fonction de conversion
    convert_md_to_html(md_file_path)
