from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class RegisterForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    direccion = StringField('Dirección', validators=[DataRequired(), Length(min=5, max=200)])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(min=7, max=20)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=1, max=100)])
    descripcion = StringField('Descripción', validators=[DataRequired(), Length(min=1, max=500)])
    precio = FloatField('Precio', validators=[DataRequired()])
    img = StringField('URL de Imagen', validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Guardar')
