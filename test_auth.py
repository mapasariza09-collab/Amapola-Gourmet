import os
from app import create_app
from app.models import User

app = create_app()
with app.app_context():
    user = User.query.filter_by(rol='super_admin').first()
    if user:
        test_pass = os.getenv('ADMIN_PASSWORD')
        result = user.check_password(test_pass)
        print(f"Usuario: {user.nombre}")
        print(f"Correo: {user.correo}")
        print(f"Rol: {user.rol}")
        print(f"Password hash: {user.password_hash}")
        print(f"check_password('{test_pass}'): {result}")
    else:
        print("Usuario no encontrado")