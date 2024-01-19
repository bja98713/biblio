# app/models.py

from app import db

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    resume_titre = db.Column(db.String(255), nullable=False)
    keywords = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    resume_article = db.Column(db.Text, nullable=True)
    html_title = db.Column(db.String(255), nullable=True)  # Nouvelle colonne pour le titre du fichier HTML

    def __init__(self, title, year, resume_titre, keywords, file_path, resume_article=None, html_title=None):
        self.title = title
        self.year = year
        self.resume_titre = resume_titre
        self.keywords = keywords
        self.file_path = file_path
        self.resume_article = resume_article
        self.html_title = html_title

    def __repr__(self):
        return f"Article('{self.title}', '{self.keywords}', '{self.file_path}', '{self.year}', '{self.resume_titre}')"

    def update_article(self, title, keywords, file_path, year, html_title, resume_titre):
        self.title = title
        self.keywords = keywords
        self.file_path = file_path
        self.year = year
        self.resume_titre = resume_titre
        self.html_title = html_title
        db.session.commit()