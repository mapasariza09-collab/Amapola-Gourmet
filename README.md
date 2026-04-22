# Proyecto Flask con Login y Registro

Este es un proyecto Flask que incluye autenticación de usuarios con login y registro.

## Instalación

1. Clona el repositorio.
2. Crea un entorno virtual: `python -m venv .venv`
3. Activa el entorno: `.venv\Scripts\activate` (Windows)
4. Instala dependencias: `pip install -r requirements.txt`

## Ejecución

Ejecuta `python run.py` para iniciar el servidor en modo debug.

## Docker

Construye la imagen: `docker build -t flask-app .`
Ejecuta: `docker run -p 5000:5000 flask-app`

## Funcionalidades

- Registro de usuarios con campos: nombre, correo, dirección, teléfono, contraseña.
- Login de usuarios.
- Página home protegida.