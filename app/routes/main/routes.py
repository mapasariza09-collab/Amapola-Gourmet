import os
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import Producto

main = Blueprint('main', __name__)

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
        precio = float(request.form.get('precio'))
        img = request.form.get('img')

        producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, img=img)
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
        producto.nombre = request.form.get('nombre')
        producto.descripcion = request.form.get('descripcion')
        producto.precio = float(request.form.get('precio'))
        producto.img = request.form.get('img')
        db.session.commit()
        flash('Producto actualizado.', 'success')
        return redirect(url_for('main.admin_productos'))
    return render_template('editar_producto.html', producto=producto)
