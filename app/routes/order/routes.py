from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from sqlalchemy import func, extract
from flask_mail import Message
from collections import defaultdict
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
        all_orders = Order.query.order_by(Order.created_at.desc()).all()
        
        # Agrupar primero por día, luego por cliente
        daily = defaultdict(lambda: defaultdict(list))
        for o in all_orders:
            day = o.created_at.date()
            daily[day][o.user_id].append(o)
        
        days_data = []
        for day in sorted(daily.keys(), reverse=True):  # más recientes primero
            day_groups = []
            for user_id, user_orders in daily[day].items():
                user = user_orders[0].user
                total = sum(oo.total_price for oo in user_orders)
                day_groups.append({
                    'user': user,
                    'orders': user_orders,
                    'total': total
                })
            days_data.append({
                'date': day,
                'clients': day_groups
            })
        
        return render_template('mis_ordenes.html', days_data=days_data, is_admin=True)
    else:
        orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
        return render_template('mis_ordenes.html', orders=orders, is_admin=False)

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

        if new_status == 'confirmado' and old_status != 'confirmado':
            msg = Message('Tu Pedido ha sido Confirmado - Amapola Gourmet',
                          recipients=[order.user.correo])
            msg.body = f'''Hola {order.user.nombre},

Tu pedido de {order.product.nombre} (Cantidad: {order.quantity}) ha sido confirmado.

Dirección de entrega: {order.delivery_address}

Método de pago: {order.payment_method}

Total: ${order.total_price}

Estamos preparando tu pedido.

Saludos,
Equipo de Amapola Gourmet
'''
            mail.send(msg)

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

@order.route('/dashboard')
@login_required
def dashboard():
    if current_user.rol not in ['admin', 'super_admin']:
        flash('No tienes permisos para acceder al dashboard.', 'danger')
        return redirect(url_for('main.home'))

    from datetime import datetime, timedelta
    now = datetime.utcnow()
    today = now.date()
    current_month = now.month
    current_year = now.year

    # Daily sales (last 30 days)
    thirty_days_ago = now - timedelta(days=30)
    daily_sales = db.session.query(
        func.date(Order.created_at).label('date'),
        func.sum(Order.total_price).label('total')
    ).filter(Order.created_at >= thirty_days_ago).group_by(func.date(Order.created_at)).order_by(func.date(Order.created_at)).all()

    # Monthly sales (last 12 months)
    twelve_months_ago = now - timedelta(days=365)
    monthly_sales = db.session.query(
        extract('year', Order.created_at).label('year'),
        extract('month', Order.created_at).label('month'),
        func.sum(Order.total_price).label('total')
    ).filter(Order.created_at >= twelve_months_ago).group_by(extract('year', Order.created_at), extract('month', Order.created_at)).order_by(extract('year', Order.created_at), extract('month', Order.created_at)).all()

    # Prepare data for charts
    daily_labels = [str(sale[0]) for sale in daily_sales]
    daily_data = [float(sale[1]) for sale in daily_sales]
    monthly_labels = [f"{int(sale[0])}-{int(sale[1]):02d}" for sale in monthly_sales]
    monthly_data = [float(sale[2]) for sale in monthly_sales]

    # Summaries
    total_today = next((sale[1] for sale in daily_sales if sale[0] == today), 0)
    total_month = next((sale[2] for sale in monthly_sales if sale[0] == current_year and sale[1] == current_month), 0)
    total_year = sum(sale[2] for sale in monthly_sales)
    avg_daily = sum(sale[1] for sale in daily_sales) / len(daily_sales) if daily_sales else 0

    return render_template('dashboard.html',
                           daily_labels=daily_labels, daily_data=daily_data,
                           monthly_labels=monthly_labels, monthly_data=monthly_data,
                           total_today=total_today, total_month=total_month,
                           total_year=total_year, avg_daily=avg_daily)

@order.route('/cart')
@login_required
def cart():
    cart_items = session.get('cart', {})
    productos = Producto.query.filter(Producto.id.in_(cart_items.keys())).all()
    cart_data = []
    total = 0

    for producto in productos:
        quantity = cart_items.get(str(producto.id), 0)
        subtotal = producto.precio * quantity
        total += subtotal
        cart_data.append({
            'producto': producto,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render_template('cart.html', cart_data=cart_data, total=total)

@order.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    producto = Producto.query.get_or_404(product_id)
    cart = session.get('cart', {})

    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + 1
    session['cart'] = cart

    flash(f'{producto.nombre} agregado al carrito.', 'success')
    return redirect(url_for('main.home'))

@order.route('/update_cart/<int:product_id>', methods=['POST'])
@login_required
def update_cart(product_id):
    quantity = request.form.get('quantity', type=int)
    if quantity is None or quantity < 0:
        quantity = 0

    cart = session.get('cart', {})
    product_id_str = str(product_id)

    if quantity == 0:
        cart.pop(product_id_str, None)
    else:
        cart[product_id_str] = quantity

    session['cart'] = cart
    return redirect(url_for('order.cart'))

@order.route('/remove_from_cart/<int:product_id>')
@login_required
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart.pop(product_id_str)
        session['cart'] = cart
        flash('Producto removido del carrito.', 'success')

    return redirect(url_for('order.cart'))

@order.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = session.get('cart', {})
    if not cart_items:
        flash('Tu carrito está vacío.', 'warning')
        return redirect(url_for('order.cart'))

    productos = Producto.query.filter(Producto.id.in_(cart_items.keys())).all()

    if request.method == 'POST':
        payment_method = request.form.get('payment_method', 'contraentrega')
        delivery_address = request.form.get('direccion_envio', '').strip()

        if payment_method not in ['transferencia', 'contraentrega', 'nequi']:
            flash('Método de pago no válido.', 'danger')
            return redirect(url_for('order.checkout'))

        if not delivery_address:
            flash('Por favor ingresa la dirección de envío.', 'danger')
            return redirect(url_for('order.checkout'))

        # Create orders for each cart item
        for producto in productos:
            quantity = cart_items.get(str(producto.id), 0)
            total_price = producto.precio * quantity

            nueva_orden = Order(
                user_id=current_user.id,
                product_id=producto.id,
                quantity=quantity,
                total_price=total_price,
                payment_method=payment_method,
                delivery_address=delivery_address,
                status='pendiente'
            )
            db.session.add(nueva_orden)

        try:
            db.session.commit()
            session.pop('cart', None)  # Clear cart after successful order
            flash('¡Órdenes realizadas exitosamente!', 'success')
            return redirect(url_for('order.mis_ordenes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al realizar las órdenes: {str(e)}', 'danger')
            return redirect(url_for('order.checkout'))

    total = sum(producto.precio * cart_items.get(str(producto.id), 0) for producto in productos)
    return render_template('checkout.html', productos=productos, cart_items=cart_items, total=total)