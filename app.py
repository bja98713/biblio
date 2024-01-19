from app import app, db
from app.models import Article

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
