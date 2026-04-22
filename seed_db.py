from app import create_app
app = create_app()
with app.app_context():
    from app import db
    from app.models import User, Producto
    from werkzeug.security import generate_password_hash
    import os
    
    # Poblar productos si no existen
    if not Producto.query.first():
        productos = [
            Producto(nombre='Hamburguesa Clásica', descripcion='Carne de res, queso cheddar, lechuga, tomate y salsa especial.', precio=12.99, img='https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400'),
            Producto(nombre='Hamburguesa BBQ', descripcion='Carne ahumada, queso, cebolla caramelizada y salsa BBQ.', precio=14.50, img='https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=400'),
            Producto(nombre='Hamburguesa Vegetariana', descripcion='Hamburguesa de garbanzo, queso, aguacate y verduras frescas.', precio=11.99, img='https://images.unsplash.com/photo-1551782450-17144efb5723?w=400'),
            Producto(nombre='Hamburguesa Deluxe', descripcion='Doble carne, doble queso, bacon y aderezos premium.', precio=16.00, img='https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=400'),
            Producto(nombre='Hamburguesa Picante', descripcion='Carne picante, jalapeños, queso pepper jack y salsa chipotle.', precio=13.50, img='https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400')
        ]
        db.session.add_all(productos)
        db.session.commit()

    # Crear usuario admin si no existe
    admin_email = os.getenv('ADMIN_EMAIL')
    admin_password = os.getenv('ADMIN_PASSWORD')
    admin_role = os.getenv('ADMIN_ROLE')
    if admin_email and admin_password and admin_role and not User.query.filter_by(correo=admin_email).first():
        admin = User(nombre='Admin', correo=admin_email, direccion='Admin Address', telefono='123456789', rol=admin_role)
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
    
    print('Seeding completed')
