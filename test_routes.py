from app import create_app
from flask_login import login_user
from app.models import User
from flask import url_for

app = create_app()
with app.app_context():
    # Buscar el usuario admin
    user = User.query.filter_by(correo='paulas@admin.com').first()

    if user:
        print(f"Usuario admin: {user.nombre} ({user.rol})")

        with app.test_request_context():
            login_user(user)
            print(f"Autenticado: {user.is_authenticated}")

            # Probar generar URLs
            try:
                admin_url = url_for('main.admin_productos')
                edit_url = url_for('main.editar_producto', id=1)
                print(f"URL admin productos: {admin_url}")
                print(f"URL editar producto: {edit_url}")
            except Exception as e:
                print(f"Error generando URLs: {e}")

            # Verificar rutas registradas
            print(f"Rutas registradas:")
            for rule in app.url_map.iter_rules():
                if 'admin' in rule.rule or 'editar' in rule.rule:
                    print(f"  {rule.rule} -> {rule.endpoint}")
    else:
        print("Usuario admin no encontrado")