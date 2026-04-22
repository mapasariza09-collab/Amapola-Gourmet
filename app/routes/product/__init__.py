from flask import Blueprint, render_template
from app.models import Producto

product = Blueprint('product', __name__)

@product.route('/productos')
def productos():
    productos = Producto.query.all()
    return render_template('productos.html', productos=productos)
