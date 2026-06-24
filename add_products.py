from app import create_app
from app.models import Producto

app = create_app()
with app.app_context():
    from app.extensions import db

    # Nuevos productos para agregar
    nuevos_productos = [
        Producto(nombre='Waffles ClÃ¡sicos', descripcion='Waffles esponjosos servidos con mantequilla y maple.', precio=8.99, img='https://images.unsplash.com/photo-1509365465985-25d11c17e446?w=400'),
        Producto(nombre='Waffles con Frutas', descripcion='Waffles con fresas frescas, bananas y miel.', precio=10.50, img='https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=400'),
        Producto(nombre='Waffles con Chocolate', descripcion='Waffles cubiertos de chocolate fundido y nueces.', precio=9.99, img='https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=400'),
        Producto(nombre='Tarta de Chocolate', descripcion='Tarta de chocolate negro con ganache y frutos rojos.', precio=7.50, img='https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400'),
        Producto(nombre='Cheesecake de Fresa', descripcion='Cheesecake cremoso con salsa de fresa fresca.', precio=6.99, img='https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=400'),
        Producto(nombre='Helado Artesanal', descripcion='Helado de vainilla con toppings variados.', precio=5.99, img='https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=400')
    ]

    productos_agregados = 0
    for producto in nuevos_productos:
        if not Producto.query.filter_by(nombre=producto.nombre).first():
            db.session.add(producto)
            productos_agregados += 1

    if productos_agregados > 0:
        db.session.commit()
        print(f"Se agregaron {productos_agregados} nuevos productos.")
    else:
        print("No se agregaron nuevos productos (ya existen).")