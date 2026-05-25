from flask import Flask
from app.extensions import db, login_manager
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'amapola123'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)

from app.models import User, Producto, Order

from app.routes.auth.routes import auth
app.register_blueprint(auth)

@app.route('/')
def home():
    return "Amapola Gourmet funcionando"

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)