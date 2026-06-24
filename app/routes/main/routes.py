import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from functools import wraps
from werkzeug.utils import secure_filename
from app import db
from app.models import Producto

main = Blueprint('main', __name__)

@main.route('/favicon.ico')
def favicon():
    return ('', 204)

def save_image(file):
    """Save uploaded image file and return the relative path"""
    if file and file.filename:
        # Ensure the uploads directory exists
        upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_dir, exist_ok=True)

        # Secure the filename
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_dir, filename)

        # Save the file
        file.save(file_path)

        # Return the relative URL path
        return f'/static/uploads/{filename}'
    return None

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin_role = os.getenv('ADMIN_ROLE', 'super_admin')
        if not current_user.is_authenticated or current_user.rol not in ['admin', 'super_admin']:
            flash('Acceso denegado. Solo para administradores.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
def home():
    productos = Producto.query.all()
    return render_template('home.html', productos=productos)

@main.route('/admin/productos')
@login_required
@admin_required
def admin_productos():
    productos = Producto.query.all()
    return render_template('admin_productos.html', productos=productos)

@main.route('/admin/producto/nuevo', methods=['GET', 'POST'])
@login_required
@admin_required
def nuevo_producto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio_str = request.form.get('precio')
        img_file = request.files.get('img')

        # Validate required fields
        if not nombre or not descripcion or not precio_str or not img_file:
            flash('Todos los campos son obligatorios.', 'danger')
            return render_template('nuevo_producto.html')

        try:
            precio = float(precio_str)
            if precio <= 0:
                flash('El precio debe ser mayor a 0.', 'danger')
                return render_template('nuevo_producto.html')
        except ValueError:
            flash('El precio debe ser un nÃºmero vÃ¡lido.', 'danger')
            return render_template('nuevo_producto.html')

        # Save the uploaded image
        img_path = save_image(img_file)
        if not img_path:
            flash('Error al guardar la imagen.', 'danger')
            return render_template('nuevo_producto.html')

        producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, img=img_path)
        db.session.add(producto)
        db.session.commit()
        flash('Producto agregado.', 'success')
        return redirect(url_for('main.admin_productos'))
    return render_template('nuevo_producto.html')

@main.route('/admin/producto/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio_str = request.form.get('precio')
        img_file = request.files.get('img')

        # Validate required fields
        if not nombre or not descripcion or not precio_str:
            flash('Nombre, descripciÃ³n y precio son obligatorios.', 'danger')
            return render_template('editar_producto.html', producto=producto)

        try:
            precio = float(precio_str)
            if precio <= 0:
                flash('El precio debe ser mayor a 0.', 'danger')
                return render_template('editar_producto.html', producto=producto)
        except ValueError:
            flash('El precio debe ser un nÃºmero vÃ¡lido.', 'danger')
            return render_template('editar_producto.html', producto=producto)

        # Handle image upload (optional for editing)
        img_path = producto.img  # Keep existing image by default
        if img_file and img_file.filename:
            new_img_path = save_image(img_file)
            if new_img_path:
                img_path = new_img_path
            else:
                flash('Error al guardar la nueva imagen. Se mantendrÃ¡ la imagen actual.', 'warning')

        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.precio = precio
        producto.img = img_path
        db.session.commit()
        flash('Producto actualizado.', 'success')
        return redirect(url_for('main.admin_productos'))
    return render_template('editar_producto.html', producto=producto)
