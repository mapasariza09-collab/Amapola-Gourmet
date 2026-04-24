from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Producto

product = Blueprint('product', __name__)

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
        img = request.form.get('img')

        # Validate required fields
        if not nombre or not descripcion or not precio_str or not img:
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

        try:
            producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, img=img)
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
        img = request.form.get('img')

        # Validate required fields
        if not nombre or not descripcion or not precio_str or not img:
            flash('Todos los campos son obligatorios.', 'danger')
            return render_template('editar_producto.html', producto=producto)

        try:
            precio = float(precio_str)
            if precio <= 0:
                flash('El precio debe ser mayor a 0.', 'danger')
                return render_template('editar_producto.html', producto=producto)
        except ValueError:
            flash('El precio debe ser un número válido.', 'danger')
            return render_template('editar_producto.html', producto=producto)

        try:
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.precio = precio
            producto.img = img
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