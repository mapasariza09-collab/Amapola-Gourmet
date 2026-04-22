from flask import Flask
from app.extensions import db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)
with app.app_context():
    db.create_all()
    print('Tables created')
