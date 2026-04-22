from flask import Flask
from .extensions import db, login_manager
from .models import User, Producto
import os

def create_app():
    app = Flask(__name__, template_folder='template')
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .routes.auth.routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .routes.main.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .routes.product.routes import product as product_blueprint
    app.register_blueprint(product_blueprint)

    with app.app_context():
        db.create_all()

        # Poblar productos si no existen
        if not Producto.query.first():
            productos = [
                Producto(nombre='Hamburguesa Clásica', descripcion='Carne de res, queso cheddar, lechuga, tomate y salsa especial.', precio=12.99, img='https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400'),
                Producto(nombre='Hamburguesa BBQ', descripcion='Carne ahumada, queso, cebolla caramelizada y salsa BBQ.', precio=14.50, img='https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=400'),
                Producto(nombre='Hamburguesa Vegetariana', descripcion='Hamburguesa de garbanzo, queso, aguacate y verduras frescas.', precio=11.99, img='https://images.unsplash.com/photo-1520072959219-c595dc870360?w=400'),
                Producto(nombre='Hamburguesa Deluxe', descripcion='Doble carne, doble queso, bacon y aderezos premium.', precio=16.00, img='https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=400'),
                Producto(nombre='Hamburguesa Picante', descripcion='Carne picante, jalapeños, queso pepper jack y salsa chipotle.', precio=13.50, img='https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400')
            ]
            db.session.add_all(productos)
            db.session.commit()

        # Crear usuario super_admin si no existe (usando variables de entorno)
        admin_name = os.getenv('ADMIN_NAME', 'paulas')
        admin_email = os.getenv('ADMIN_EMAIL', 'paulas@admin.com')
        admin_password = os.getenv('ADMIN_PASSWORD', 'paulas@')
        admin_role = os.getenv('ADMIN_ROLE', 'super_admin')

        if not User.query.filter_by(correo=admin_email).first():
            admin = User(nombre=admin_name, correo=admin_email, direccion='Admin Address', telefono='123456789', rol=admin_role)
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()

    return app
