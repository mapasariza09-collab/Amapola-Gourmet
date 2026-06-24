ï»¿from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('ContraseÃ±a', validators=[DataRequired()])
    submit = SubmitField('Iniciar SesiÃ³n')

class RegisterForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    direccion = StringField('DirecciÃ³n', validators=[DataRequired(), Length(min=5, max=200)])
    telefono = StringField('TelÃ©fono', validators=[DataRequired(), Length(min=7, max=20)])
    password = PasswordField('ContraseÃ±a', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar ContraseÃ±a', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=1, max=100)])
    descripcion = StringField('DescripciÃ³n', validators=[DataRequired(), Length(min=1, max=500)])
    precio = FloatField('Precio', validators=[DataRequired()])
    img = StringField('URL de Imagen', validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Guardar')
