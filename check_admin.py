from app import create_app
from flask_login import login_user
from app.models import User

app = create_app()
with app.app_context():
    # Buscar el usuario admin
    user = User.query.filter_by(correo='paulas@admin.com').first()

    if user:
        print(f"Usuario encontrado:")
        print(f"- Nombre: {user.nombre}")
        print(f"- Email: {user.correo}")
        print(f"- Rol: {user.rol}")
        print(f"- Tiene permisos de admin: {user.rol in ['admin', 'super_admin']}")

        # Intentar hacer login
        from flask import Flask
        from flask_login import LoginManager
        login_manager = LoginManager()
        login_manager.init_app(app)

        with app.test_request_context():
            login_user(user)
            print(f"- Login exitoso: {user.is_authenticated}")
    else:
        print("Usuario admin no encontrado")

    # Verificar productos
    productos = user.__class__.__bases__[0].__subclasses__()[0].query.all()
    print(f"\nProductos en BD: {len(productos)}")
    for p in productos[:3]:  # Mostrar solo los primeros 3
        print(f"- {p.nombre}")