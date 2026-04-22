from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app import db
from app.models import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')
        password = request.form.get('password')

        user = User.query.filter_by(correo=correo).first()
        if user:
            flash('El correo ya está registrado.', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(nombre=nombre, correo=correo, direccion=direccion, telefono=telefono, rol='cliente')
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Cuenta creada exitosamente.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')

        user = User.query.filter_by(correo=correo).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Credenciales inválidas.', 'danger')

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
