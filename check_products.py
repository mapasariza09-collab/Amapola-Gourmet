from app import create_app
from app.models import Producto

app = create_app()
with app.app_context():
    productos = Producto.query.all()
    print(f"Productos en la base de datos: {len(productos)}")
    for producto in productos:
        print(f"- {producto.nombre}: ${producto.precio}")