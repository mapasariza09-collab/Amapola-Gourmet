from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask_mail import Message
from app import db, mail
from app.models import Producto, Order

order = Blueprint('order', __name__)

@order.route('/ordenar', methods=['GET', 'POST'])
@login_required
def ordenar():
    productos = Producto.query.all()
    selected_product_id = request.args.get('product_id', type=int)

    if request.method == 'POST':
        product_id = request.form.get('product_id', type=int)
        quantity = request.form.get('quantity', type=int, default=1)
        payment_method = request.form.get('payment_method', 'contraentrega')
        delivery_address = request.form.get('direccion_envio', '').strip()

        if not product_id or not quantity or quantity <= 0:
            flash('Selecciona un producto y una cantidad válida.', 'danger')
            return render_template('order.html', productos=productos, selected_product_id=selected_product_id)

        if payment_method not in ['transferencia', 'contraentrega', 'nequi']:
            flash('Método de pago no válido.', 'danger')
            return render_template('order.html', productos=productos, selected_product_id=selected_product_id)

        if not delivery_address:
            flash('Por favor ingresa la dirección de envío.', 'danger')
            return render_template('order.html', productos=productos, selected_product_id=selected_product_id)

        if not delivery_address:
            flash('Por favor ingresa la dirección de envío.', 'danger')
            return render_template('order.html', productos=productos, selected_product_id=selected_product_id)

        if payment_method not in ['transferencia', 'contraentrega', 'nequi']:
            flash('Método de pago no válido.', 'danger')
            return render_template('order.html', productos=productos, selected_product_id=selected_product_id)

        producto = Producto.query.get_or_404(product_id)
        total_price = producto.precio * quantity

        nueva_orden = Order(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity,
            total_price=total_price,
            payment_method=payment_method,
            delivery_address=delivery_address,
            status='pendiente'
        )

        try:
            db.session.add(nueva_orden)
            db.session.commit()
            flash('¡Orden realizada exitosamente!', 'success')
            return redirect(url_for('main.home'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al realizar la orden: {str(e)}', 'danger')

    return render_template('order.html', productos=productos, selected_product_id=selected_product_id)

@order.route('/mis-ordenes')
@login_required
def mis_ordenes():
    if current_user.rol in ['admin', 'super_admin']:
        orders = Order.query.order_by(Order.created_at.desc()).all()
    else:
        orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('mis_ordenes.html', orders=orders)

@order.route('/update_order/<int:order_id>', methods=['POST'])
@login_required
def update_order(order_id):
    if current_user.rol not in ['admin', 'super_admin']:
        flash('No tienes permisos para esta acción.', 'danger')
        return redirect(url_for('order.mis_ordenes'))

    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')

    if new_status in ['pendiente', 'confirmado', 'enviado', 'entregado', 'cancelado']:
        old_status = order.status
        order.status = new_status
        db.session.commit()

        if new_status == 'enviado' and old_status != 'enviado':
            msg = Message('Tu Pedido ha sido Enviado - Amapola Gourmet',
                          recipients=[order.user.correo])
            msg.body = f'''Hola {order.user.nombre},

Tu pedido de {order.product.nombre} (Cantidad: {order.quantity}) ha sido enviado.

Dirección de entrega: {order.delivery_address}

Método de pago: {order.payment_method}

Total: ${order.total_price}

Gracias por tu compra.

Saludos,
Equipo de Amapola Gourmet
'''
            mail.send(msg)

        flash('Estado de la orden actualizado.', 'success')
    else:
        flash('Estado no válido.', 'danger')

    return redirect(url_for('order.mis_ordenes'))