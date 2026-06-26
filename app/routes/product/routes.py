from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app.extensions import db
from app.models import Producto

product = Blueprint('product', __name__)

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

@product.route('/productos')
def productos():
    productos = Producto.query.all()
    return render_template('productos.html', productos=productos)

@product.route('/productos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    if current_user.rol not in ['admin', 'super_admin']:
        flash('No tienes permisos para crear productos.', 'danger')
        return redirect(url_for('product.productos'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio_str = request.form.get('precio')
        img_file = request.files.get('img')

        # Validate required fields
        if not nombre or not descripcion or not precio_str or not img_file:
            flash('Todos los campos son obligatorios.', 'danger')
            return render_template('editar_producto.html', producto=None)

        try:
            precio = float(precio_str)
            if precio <= 0:
                flash('El precio debe ser mayor a 0.', 'danger')
                return render_template('editar_producto.html', producto=None)
        except ValueError:
            flash('El precio debe ser un número válido.', 'danger')
            return render_template('editar_producto.html', producto=None)

        # Save the uploaded image
        img_path = save_image(img_file)
        if not img_path:
            flash('Error al guardar la imagen.', 'danger')
            return render_template('editar_producto.html', producto=None)

        try:
            producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, img=img_path)
            db.session.add(producto)
            db.session.commit()
            flash('Producto creado exitosamente.', 'success')
            return redirect(url_for('product.productos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el producto: {str(e)}', 'danger')
            return render_template('editar_producto.html', producto=None)

    return render_template('editar_producto.html', producto=None)

@product.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    if current_user.rol not in ['admin', 'super_admin']:
        flash('No tienes permisos para editar productos.', 'danger')
        return redirect(url_for('product.productos'))

    producto = Producto.query.get_or_404(id)

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio_str = request.form.get('precio')
        img_file = request.files.get('img')

        # Validate required fields
        if not nombre or not descripcion or not precio_str:
            flash('Nombre, descripción y precio son obligatorios.', 'danger')
            return render_template('editar_producto.html', producto=producto)

        try:
            precio = float(precio_str)
            if precio <= 0:
                flash('El precio debe ser mayor a 0.', 'danger')
                return render_template('editar_producto.html', producto=producto)
        except ValueError:
            flash('El precio debe ser un número válido.', 'danger')
            return render_template('editar_producto.html', producto=producto)

        # Handle image upload (optional for editing)
        img_path = producto.img  # Keep existing image by default
        if img_file and img_file.filename:
            new_img_path = save_image(img_file)
            if new_img_path:
                img_path = new_img_path
            else:
                flash('Error al guardar la nueva imagen. Se mantendrá la imagen actual.', 'warning')

        try:
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.precio = precio
            producto.img = img_path
            db.session.commit()
            flash('Producto actualizado.', 'success')
            return redirect(url_for('product.productos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el producto: {str(e)}', 'danger')
            return render_template('editar_producto.html', producto=producto)

    return render_template('editar_producto.html', producto=producto)

@product.route('/productos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    if current_user.rol not in ['admin', 'super_admin']:
        flash('No tienes permisos para eliminar productos.', 'danger')
        return redirect(url_for('product.productos'))

    producto = Producto.query.get_or_404(id)
    try:
        db.session.delete(producto)
        db.session.commit()
        flash('Producto eliminado.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el producto: {str(e)}', 'danger')
    return redirect(url_for('product.productos'))
