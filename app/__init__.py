from flask import Flask
from .extensions import db, login_manager, csrf, mail
from .models import User, Producto, Order
import os
from sqlalchemy import text

def create_app():
    app = Flask(__name__, template_folder='template')
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'mapasariza09@gmail.com'
    app.config['MAIL_PASSWORD'] = 'rnpu qnqk alnk gmnq'
    app.config['MAIL_DEFAULT_SENDER'] = 'mapasariza09@gmail.com'

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    login_manager.login_view = 'auth.login'

    from .routes.auth.routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .routes.main.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .routes.product.routes import product as product_blueprint
    app.register_blueprint(product_blueprint)

    from .routes.order.routes import order as order_blueprint
    app.register_blueprint(order_blueprint)

    with app.app_context():
        db.create_all()

        # Poblar productos si no existen
        if not db.session.execute(text("SELECT id FROM producto LIMIT 1")).first():
            productos = [
                Producto(nombre='Hamburguesa La Salvaje', descripcion='Carne de res premium con salsa picante artesanal, jalapeños, cebolla morada y aderezos especiales.', precio=18.99, img='https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400', categoria='comida'),
                Producto(nombre='Hamburguesa Clásica', descripcion='Carne de res, queso cheddar, lechuga, tomate y salsa especial.', precio=15.99, img='https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400', categoria='comida'),
                Producto(nombre='Hamburguesa Delirio', descripcion='Doble carne premium, doble queso, bacon artesanal, piña asada y salsa delirante.', precio=22.99, img='https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=400', categoria='comida'),
                Producto(nombre='Soda de Lulo', descripcion='Refresco natural de lulo colombiano, refrescante y exótico.', precio=4.99, img='https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=400', categoria='bebida'),
                Producto(nombre='Soda de Maracuyá', descripcion='Refresco de maracuyá colombiano, dulce y ácido perfecto.', precio=4.99, img='https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=400', categoria='bebida'),
                Producto(nombre='Soda de Frutos Rojos', descripcion='Mezcla refrescante de frutos rojos colombianos: mora, fresa y frambuesa.', precio=4.99, img='https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=400', categoria='bebida'),
                Producto(nombre='Waffle Gold', descripcion='Waffle premium dorado con chocolate belga, nueces caramelizadas y crema chantilly.', precio=14.99, img='https://images.unsplash.com/photo-1509365465985-25d11c17e446?w=400', categoria='postre'),
                Producto(nombre='Copete + Cheesecake', descripcion='Helado suave colombiano con cheesecake cremoso y topping de frutas frescas.', precio=12.99, img='https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=400', categoria='postre'),
                Producto(nombre='Waffle Crunch', descripcion='• Base crujiente de yuca al estilo pandebono\n• Dedos de pollo apanados en panko y ajonjolí negro\n• Acompañado de refrescante salsa tzatziki\n• Finalizado con un toque de miel picante que eleva la experiencia', precio=13.99, img='https://media.igram.world/get?__sig=UQHHKv-Gcu2Si9aH63ejig&__expires=1777170101&uri=https%3A%2F%2Fscontent-iad3-1.cdninstagram.com%2Fv%2Ft51.2885-15%2F496446382_17867174637373330_134404182676226060_n.jpg%3Fstp%3Ddst-jpg_e35_p1080x1080_sh0.08_tt6%26_nc_ht%3Dscontent-iad3-1.cdninstagram.com%26_nc_cat%3D110%26_nc_oc%3DQ6cZ2gEn7rBCfPYU4srYctB1ounz3mzDguCmu1RfRWwtbhZqW9AgF6cxpg8GniOfHD4qtGbdiu09F5UyDi-mhkvG9UvO%26_nc_ohc%3DTFU45GqmLdYQ7kNvwGXFLL-%26_nc_gid%3D9pDd5DqMwZBPgfDFGye0Ug%26edm%3DANTKIIoBAAAA%26ccb%3D7-5%26oh%3D00_Af2iEcAjv0oB17jARGZxlDIsKZjVBzibu0tQaiYunx7UxA%26oe%3D69F32548%26_nc_sid%3Dd885a2&filename=496446382_17867174637373330_134404182676226060_n.jpg', categoria='postre'),
                Producto(nombre='Waffle Amapola', descripcion='Waffle artesanal con matcha premium, frutas frescas y yogurt griego.', precio=16.99, img='https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=400', categoria='postre'),
                Producto(nombre='Waffle Encanto', descripcion='Waffle mágico con chocolate blanco, frambuesas y almendras tostadas.', precio=15.99, img='https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=400', categoria='postre')
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
