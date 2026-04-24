# 🍔 Hamburguesas Deliciosas

Una aplicación web Flask para gestión de productos de una hamburguesería con autenticación de usuarios.

## 📋 Características

- **Autenticación de usuarios**: Registro y login seguro
- **Gestión de productos**: Crear, editar, eliminar y visualizar productos
- **Sistema de roles**: Usuarios normales y administradores
- **Interfaz responsiva**: Diseño moderno con Bootstrap
- **Base de datos SQLite**: Persistencia de datos simple y eficiente

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clona el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd paula
   ```

2. **Crea un entorno virtual:**
   ```bash
   python -m venv .venv
   ```

3. **Activa el entorno virtual:**
   ```bash
   # Windows
   .venv\Scripts\activate

   # Linux/Mac
   source .venv/bin/activate
   ```

4. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## 📦 Dependencias

```
Flask==2.3.3          # Framework web
Flask-SQLAlchemy==3.0.5  # ORM para base de datos
Flask-Login==0.6.3    # Gestión de sesiones de usuario
Flask-WTF==1.2.2      # Formularios web seguros
Werkzeug==2.3.7       # Utilidades WSGI
```

## ▶️ Ejecución

### Modo desarrollo
```bash
python run.py
```

La aplicación estará disponible en: http://127.0.0.1:5000

### Con Docker

1. **Construye la imagen:**
   ```bash
   docker build -t hamburguesas-deliciosas .
   ```

2. **Ejecuta el contenedor:**
   ```bash
   docker run -p 5000:5000 hamburguesas-deliciosas
   ```

## 👥 Usuarios por defecto

- **Administrador**: `paulas` / `paulas@`
- **Email admin**: `paulas@admin.com`

## 📁 Estructura del proyecto

```
paula/
├── app/
│   ├── __init__.py          # Configuración de la aplicación Flask
│   ├── extensions.py        # Extensiones Flask (DB, Login, CSRF)
│   ├── models/              # Modelos de base de datos
│   │   ├── __init__.py      # Definición de modelos User y Producto
│   ├── routes/              # Rutas de la aplicación
│   │   ├── auth/            # Autenticación (login/registro)
│   │   ├── main/            # Rutas principales y admin
│   │   └── product/         # Gestión de productos
│   └── template/            # Plantillas HTML
├── instance/                # Base de datos SQLite
├── requirements.txt         # Dependencias Python
├── run.py                   # Punto de entrada de la aplicación
└── README.md               # Este archivo
```

## 🔧 Funcionalidades

### Para usuarios normales:
- Ver productos disponibles
- Registro e inicio de sesión

### Para administradores:
- Todas las funciones de usuario normal
- Crear nuevos productos
- Editar productos existentes
- Eliminar productos
- Panel de administración

## 🛠️ Scripts útiles

- `python add_products.py`: Agrega productos de ejemplo a la base de datos
- `python seed_db.py`: Inicializa la base de datos con datos de prueba
- `python check_admin.py`: Verifica la configuración del administrador

## 🔒 Variables de entorno

Puedes configurar estas variables de entorno:

- `ADMIN_NAME`: Nombre del administrador (default: 'paulas')
- `ADMIN_EMAIL`: Email del administrador (default: 'paulas@admin.com')
- `ADMIN_PASSWORD`: Contraseña del administrador (default: 'paulas@')
- `ADMIN_ROLE`: Rol del administrador (default: 'super_admin')

## 📝 Notas de desarrollo

- La aplicación usa SQLite para desarrollo
- En producción, considera usar PostgreSQL o MySQL
- Las imágenes de productos se almacenan como URLs externas
- El sistema incluye validación CSRF para seguridad de formularios

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.