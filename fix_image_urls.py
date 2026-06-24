from app import create_app
from app.models import Producto

app = create_app()
with app.app_context():
    from app.extensions import db

    # Update expired Instagram image URLs with working food images
    image_updates = {
        'Copete citeÃ±o + cheesecake': 'https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=400',  # Cheesecake image
        'Waffle Crunch': 'https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=400',  # Waffles with fruit
        'Waffle Encanto': 'https://images.unsplash.com/photo-1509365465985-25d11c17e446?w=400',  # Classic waffles
        'Waffle Amapola': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=400',  # Waffles with chocolate
        'Waffle Gold': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400'  # Golden waffles
    }

    updated_count = 0
    for nombre, nueva_imagen in image_updates.items():
        producto = Producto.query.filter_by(nombre=nombre).first()
        if producto:
            producto.img = nueva_imagen
            updated_count += 1
            print(f"Updated {nombre} with new image URL")

    if updated_count > 0:
        db.session.commit()
        print(f"\nSuccessfully updated {updated_count} product images.")
    else:
        print("No products were updated.")

    # Show current image URLs for verification
    print("\nCurrent image URLs for dessert products:")
    productos = Producto.query.all()
    for producto in productos:
        if any(name.lower() in producto.nombre.lower() for name in ['copete', 'cheesecake', 'waffle']):
            print(f"- {producto.nombre}: {producto.img}")