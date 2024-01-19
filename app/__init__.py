# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
import os
#from app import app, db
#from app import routes  # Import routes after initializing 'app' and 'db'
#from flask_wtf.csrf import CSRFProtect  # Importez CSRFProtect
#from flask_seasurf import SeaSurf

app = Flask(__name__)
#csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = 'Djibouti29./*$'  # Remplacez par une vraie clé secrète
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'app', 'uploads')  # Chemin vers le dossier d'upload
db = SQLAlchemy(app)
#migrate = Migrate(app, db)

from app import routes  # Assurez-vous d'avoir cette ligne à la fin du fichier
