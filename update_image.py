from app import create_app
from app.models import Producto

app = create_app()
with app.app_context():
    vegetariana = Producto.query.filter_by(nombre='Hamburguesa Vegetariana').first()
    if vegetariana:
        vegetariana.img = 'https://images.unsplash.com/photo-1520072959219-c595dc870360?w=400'
        from app.extensions import db
        db.session.commit()
        print("Imagen de Hamburguesa Vegetariana actualizada.")
    else:
        print("Producto no encontrado.")