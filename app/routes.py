# app/routes.py

from flask import render_template, request, redirect, url_for, send_file
from app import app, db
from app.models import Article
from flask import send_from_directory
import os
from app.forms import ArticleForm  # Assurez-vous d'importer le formulaire approprié
import markdown
from werkzeug.utils import secure_filename
from collections import Counter


HTML_FOLDER = 'app/html'
MARKDOWN_FOLDER = 'app/markdown'


@app.route('/')
def index():
    articles = Article.query.all()
    return render_template('index.html', articles=articles)

@app.route('/keyword_stats')
def keyword_stats():
    # Récupérer tous les articles depuis la base de données
    articles = Article.query.all()

    # Extraire tous les mots-clés et les stocker dans une liste
    all_keywords = [article.keywords for article in articles]

    # Séparer les mots-clés en une liste d'éléments individuels
    all_keywords_list = [keyword.strip() for keywords in all_keywords for keyword in keywords.split(',')]

    # Utiliser Counter pour compter la fréquence de chaque mot-clé
    keyword_counts = Counter(all_keywords_list)

    # Tri des mots-clés par ordre alphabétique
    sorted_keyword_counts = dict(sorted(keyword_counts.items()))

    # Passer les résultats au modèle
    return render_template('keyword_stats.html', keyword_counts=keyword_counts)
    #return render_template('keyword_stats.html', keyword_counts=keyword_counts, sorted_all_keywords_list=sorted_all_keywords_list)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_keywords = request.form.get('search_keywords', '')
        # Séparez les mots-clés saisis
        search_keywords_list = [keyword.strip() for keyword in search_keywords.split(',')]
        
        # Recherche des articles qui contiennent au moins l'un des mots-clés
        articles = Article.query.filter(Article.keywords.ilike('%{}%'.format(search_keywords_list[0])))
        for keyword in search_keywords_list[1:]:
            articles = articles.filter(Article.keywords.ilike('%{}%'.format(keyword)))

        articles = articles.all()

        return render_template('search_results.html', search_keywords=search_keywords, articles=articles)

    return render_template('search.html')

@app.route('/keyword/<keyword>')
def articles_by_keyword(keyword):
    # Récupérer les articles qui contiennent le mot-clé spécifié
    articles = Article.query.filter(Article.keywords.ilike(f"%{keyword}%")).all()

    return render_template('articles_by_keyword.html', keyword=keyword, articles=articles)

@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    if request.method == 'POST':
        title = request.form['title']
        keywords = request.form['keywords']
        file = request.files['file']
        year = request.form['year']
        resume_titre = request.form['resume_titre']
        html_title = request.form['html_title']  # Nouveau champ pour le titre du fichier HTML

        # Sauvegarde du fichier PDF
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(file_path)

        # Récupérer le contenu Markdown du champ resume_article
        markdown_content = request.form['resume_article']
        
        # Récupérer le titre pour la création des fichiers
        html_title = request.form['html_title']

        # Créer le nom du fichier Markdown
        markdown_filename = f"article_{html_title.lower().replace(' ', '_')}.md"
        markdown_filepath = os.path.join(MARKDOWN_FOLDER, markdown_filename)

        # Enregistrer le contenu Markdown dans un fichier
        with open(markdown_filepath, 'w', encoding='utf-8') as markdown_file:
            markdown_file.write(markdown_content)

        # Convertir le fichier Markdown en HTML
        html_content = markdown.markdown(markdown_content)

        # Créer le nom du fichier HTML
        #html_filename = f"article_{html_title.lower().replace(' ', '_')}.html"
        html_filename = f"article_{html_title.lower().replace(' ', '_')}.html"
        html_filepath = os.path.join(HTML_FOLDER, html_filename)

        # Enregistrer le contenu HTML dans un fichier (facultatif)
        with open(html_filepath, 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)

        #Génération du fichier HTML à partir du contenu Markdown du champ resume_article
        #markdown_content = request.form['resume_article']
        #html_content = markdown.markdown(markdown_content)
        html_content_with_title = f"<h1>{html_title}</h1>\n{html_content}"

        # Nom du fichier HTML
        #html_filename = f"article_{title.lower().replace(' ', '_')}.html"
        #html_filepath = os.path.join(HTML_FOLDER, html_filename)

        try:
            with open(html_filepath, 'w', encoding='utf-8') as html_file:
                html_file.write(html_content_with_title)
            print(f"Fichier HTML créé avec succès : {html_filepath}")
        except Exception as e:
            print(f"Erreur lors de la création du fichier HTML : {e}")

        # Supprimer le fichier Markdown une fois que le fichier HTML est créé
        if os.path.exists(markdown_filepath):
           os.remove(markdown_filepath)

        # Ajout de l'article à la base de données
        article = Article(title=title, year=year, resume_titre=resume_titre, keywords=keywords, file_path=file_path, resume_article=markdown_content, html_title=html_title)
        db.session.add(article)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_article.html')


@app.route('/resume_article/<int:article_id>')
def resume_article(article_id):
    article = Article.query.get(article_id)

    if article:
        return render_template('resume_article.html', article=article)
    else:
        return "Article non trouvé", 404

@app.route('/delete_article/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    article = Article.query.get(article_id)

    if article:
        # Supprimer le fichier associé (HTML)
        delete_html_file(article)

        # Supprimer le fichier résumé
        if os.path.exists(article.file_path):
            os.remove(article.file_path)

        # Supprimer l'article de la base de données
        db.session.delete(article)
        db.session.commit()

    return redirect(url_for('index'))

def delete_html_file(article):
    
    #html_filename = f"article_{article.title.lower().replace(' ', '_')}.html"
    html_filename = f"article_{article.html_title.lower().replace(' ', '_')}.html"
    html_filepath = os.path.join(HTML_FOLDER, html_filename)

    try:
        # Supprimer le fichier HTML s'il existe
        if os.path.exists(html_filepath):
            os.remove(html_filepath)
            print(f"Fichier HTML supprimé avec succès : {html_filepath}")
        else:
            print(f"Le fichier HTML n'existe pas : {html_filepath}")
    except Exception as e:
        print(f"Erreur lors de la suppression du fichier HTML : {e}")


@app.route('/read_file/<int:article_id>')
def read_file(article_id):
    article = Article.query.get(article_id)

    if article:
        return send_file(article.file_path, as_attachment=True, download_name=f"{article.title}.pdf")
    else:
        return "Fichier non trouvé", 404

@app.route('/edit_article/<int:article_id>', methods=['GET', 'POST'])
#@csrf.exempt
def edit_article(article_id):
    article = Article.query.get(article_id)
    form = ArticleForm(obj=article)

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(article)  # Met à jour l'objet Article avec les données du formulaire
        article.update_article(
            form.title.data,
            form.keywords.data,
            form.file_path.data,
            form.year.data,
            form.html_title.data,
            form.resume_titre.data
        )
        return redirect(url_for('index'))

    return render_template('edit_article.html', title='Edit Article', form=form, article=article)

@app.route('/transform', methods=['GET', 'POST'])
def transform():
    html_content = None  # Déclarer la variable à l'extérieur du bloc try

    if request.method == 'POST':
        if 'md_file' not in request.files:
            return "Aucun fichier Markdown choisi", 400

        md_file = request.files['md_file']

        if md_file.filename == '':
            return "Aucun fichier Markdown choisi", 400

        try:
            # Assurez-vous que le fichier est au format Markdown
            if md_file and md_file.filename.endswith('.md'):
                # Lisez le contenu du fichier Markdown
                md_content = md_file.read().decode('utf-8')

                # Convertissez le contenu Markdown en HTML
                html_content = Markup(markdown.markdown(md_content))

                # Affichez le contenu HTML dans la page
                return render_template('transform_result.html', html_content=html_content)

            return "Format de fichier non pris en charge. Veuillez choisir un fichier Markdown (.md)", 400
        except Exception as e:
            return f"Une erreur s'est produite : {e}", 500

    return render_template('transform.html')

    #return render_template('transform_result.html', html_content=html_content)

if __name__ == '__main__':
    app.run(debug=True)
