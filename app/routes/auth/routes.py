from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from flask_mail import Message
from app import db, mail
from app.models import User, Producto

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
        identificador = request.form.get('correo')
        password = request.form.get('password')

        # Buscar usuario por correo o por nombre
        user = User.query.filter((User.correo == identificador) | (User.nombre == identificador)).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Credenciales inválidas.', 'danger')

    productos = Producto.query.all()
    return render_template('login.html', productos=productos)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        correo = request.form.get('correo')
        user = User.query.filter_by(correo=correo).first()
        if user:
            token = user.get_reset_token()
            msg = Message('Recuperación de Contraseña - Amapola Gourmet',
                          recipients=[correo])
            msg.body = f'''Hola {user.nombre},

Has solicitado recuperar tu contraseña para Amapola Gourmet.

Para restablecer tu contraseña, visita el siguiente enlace:

{url_for('auth.reset_password', token=token, _external=True)}

Este enlace expirará en 30 minutos.

Si no solicitaste este cambio, ignora este mensaje.

Saludos,
Equipo de Amapola Gourmet
'''
            mail.send(msg)
        return redirect(url_for('auth.login'))
    return render_template('forgot_password.html')

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_token(token)
    if user is None:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        password = request.form.get('password')
        user.set_password(password)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html')
@auth.route('/')
def home():
    return redirect(url_for('auth.login'))