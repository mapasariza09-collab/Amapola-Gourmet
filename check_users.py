from app import create_app
from app.models import User

app = create_app()
with app.app_context():
    users = User.query.all()
    print(f"Usuarios en la base de datos: {len(users)}")
    for user in users:
        print(f"- Nombre: {user.nombre}")
        print(f"  Email: {user.correo}")
        print(f"  Rol: {user.rol}")
        print(f"  DirecciÃ³n: {user.direccion}")
        print()