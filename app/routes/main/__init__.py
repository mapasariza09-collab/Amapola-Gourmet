from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Producto

main = Blueprint('main', __name__)

@main.route('/')
def home():
    productos = Producto.query.all()
    return render_template('home.html', productos=productos)
