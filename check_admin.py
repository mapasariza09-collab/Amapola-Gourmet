from app import create_app
from app.models import User
from app.extensions import db
import os

app = create_app()
with app.app_context():
    admin_email = os.getenv('ADMIN_EMAIL', 'paulas@admin.com')
    admin_name = os.getenv('ADMIN_NAME', 'paulas')
    admin = User.query.filter_by(correo=admin_email).first()
    if admin:
        print(f"Super admin encontrado: {admin.nombre}, correo: {admin.correo}")
    else:
        print("Super admin no existe. Creando...")
        admin_password = os.getenv('ADMIN_PASSWORD', 'paulas@')
        admin_role = os.getenv('ADMIN_ROLE', 'super_admin')
        admin = User(nombre=admin_name, correo=admin_email, direccion='Admin Address', telefono='123456789', rol=admin_role)
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
        print("Super admin creado!")