from app import create_app
from app.models import Producto

app = create_app()
with app.app_context():
    productos = Producto.query.all()
    print("Productos con sus URLs de imagen:")
    for producto in productos:
        if any(name.lower() in producto.nombre.lower() for name in ['copete', 'cheesecake', 'waffle']):
            print(f"- {producto.nombre}: {producto.img}")