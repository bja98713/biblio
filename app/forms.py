# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired

class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    keywords = StringField('Keywords', validators=[DataRequired()])
    file_path = StringField('File Path', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    resume_titre = TextAreaField('Resume', validators=[DataRequired()])
    html_title = TextAreaField('Resume Titre', validators=[DataRequired()])
    resume_article = TextAreaField('Resume Article', validators=[DataRequired()])
