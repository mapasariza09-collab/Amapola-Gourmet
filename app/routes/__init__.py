import os
from flask import Flask
from app.extensions import db, login_manager

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'amapola_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    # IMPORTAR MODELOS
    from app.models import User, Producto, Order

    # IMPORTAR RUTAS
    from app.routes.auth.routes import auth
    app.register_blueprint(auth)

    # CREAR TABLAS
    with app.app_context():
        db.create_all()

    return app