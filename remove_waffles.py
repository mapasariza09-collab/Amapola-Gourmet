from app import create_app
from app.models import Producto

app = create_app()
with app.app_context():
    from app.extensions import db

    # Waffles a eliminar
    waffles_a_eliminar = [
        'Waffles Clásicos',
        'Waffles con Frutas',
        'Waffles con Chocolate'
    ]

    productos_eliminados = 0
    for nombre in waffles_a_eliminar:
        producto = Producto.query.filter_by(nombre=nombre).first()
        if producto:
            db.session.delete(producto)
            productos_eliminados += 1

    if productos_eliminados > 0:
        db.session.commit()
        print(f"Se eliminaron {productos_eliminados} productos de waffles.")
    else:
        print("No se encontraron productos de waffles para eliminar.")

    # Mostrar productos restantes
    productos_restantes = Producto.query.all()
    print(f"\nProductos restantes ({len(productos_restantes)}):")
    for p in productos_restantes:
        print(f"- {p.nombre}")