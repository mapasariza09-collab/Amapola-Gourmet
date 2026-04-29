from app.extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    rol = db.Column(db.String(50), nullable=False, default='cliente')  # 'admin', 'cliente', 'empleado'
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec=1800):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps(self.id, salt='password-reset-salt')

    @staticmethod
    def verify_reset_token(token, max_age=1800):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, salt='password-reset-salt', max_age=max_age)
        except:
            return None
        return User.query.get(user_id)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    img = db.Column(db.String(200), nullable=False)  # URL de imagen
    # categoria = db.Column(db.String(50), nullable=False, default='comida')  # 'comida', 'bebida', 'postre'

    def __repr__(self):
        return f"Producto('{self.nombre}', '{self.precio}')"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    total_price = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20), nullable=False, default='contraentrega')  # 'transferencia', 'contraentrega', 'nequi'
    delivery_address = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pendiente')  # 'pendiente', 'confirmado', 'enviado', 'entregado', 'cancelado'
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    product = db.relationship('Producto', backref=db.backref('orders', lazy=True))

    def __repr__(self):
        return f"Order('{self.id}', '{self.user.nombre}', '{self.product.nombre}', '{self.payment_method}', '{self.delivery_address[:30]}...', '{self.status}')"
