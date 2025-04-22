from flask import Blueprint, render_template,flash,redirect,request,jsonify
from .models import Producto, Carrito, Orden,Cliente
from flask_login import login_required,current_user
from . import db 
import traceback
views = Blueprint('views', __name__)




@views.route('/')
def home():
    items = Producto.query.filter_by(flash_sale=True)
    return render_template('home.html', items=items, carrito = Carrito.query.filter_by(cliente_link=current_user.id).all()
                           if current_user.is_authenticated else [])


@views.route('/add-to-cart/<int:item_id>')
@login_required
def add_to_cart(item_id):
    item_to_add = Producto.query.get(item_id)
    item_exists = Carrito.query.filter_by(producto_link=item_id, cliente_link=current_user.id).first()
    if item_exists:
       try:
           item_exists.cantidad = item_exists.cantidad + 1
           db.session.commit()
           flash(f'Cantidad de { item_exists.producto.nombre_producto } ha sido actualizado')
           return redirect(request.referrer)
       except Exception as e:
           print('Cantidad no actualizada', e)
           flash(f'Cantidad de { item_exists.producto.nombre_producto } no actualizado')
           return redirect(request.referrer)
       
    new_cart_item = Carrito()
    new_cart_item.cantidad = 1
    new_cart_item.producto_link = item_to_add.id # type: ignore
    new_cart_item.cliente_link = current_user.id 

    try:
     db.session.add(new_cart_item)
     db.session.commit()
     flash(f'{new_cart_item.producto.nombre_producto} agregado')
    except Exception as e:
     print('Item no agregado al carrito', e)
     flash(f'{new_cart_item.producto.nombre_producto} no se ha agregado correctamente')
    
    return redirect(request.referrer)


@views.route('/cart')
@login_required
def show_cart():
    carrito = Carrito.query.filter_by(cliente_link=current_user.id).all()
    
    amount = 0
    for item in carrito:
        amount += item.producto.precio_actual * item.cantidad

    return render_template('cart.html', carrito=carrito, amount=amount, total=amount + 200)

@views.route('/pluscart')
@login_required
def plus_cart():
   if request.method == 'GET':
      carrito_id = request.args.get('carrito_id')
      carrito_item = Carrito.query.get(carrito_id)
      carrito_item.cantidad = carrito_item.cantidad + 1
      db.session.commit()

      carrito = Carrito.query.filter_by(cliente_link=current_user.id).all()

      amount = 0

      for item in carrito:
        amount += item.producto.precio_actual * item.cantidad

        data= {
        'cantidad': carrito_item.cantidad,
        'amount': amount,
        'total': amount + 200
      }

      return jsonify(data)
   


@views.route('/minuscart')
@login_required
def minus_cart():
   if request.method == 'GET':
      carrito_id = request.args.get('carrito_id')
      carrito_item = Carrito.query.get(carrito_id)
      carrito_item.cantidad = carrito_item.cantidad - 1
      db.session.commit()

      carrito = Carrito.query.filter_by(cliente_link=current_user.id).all()

      amount = 0

      for item in carrito:
        amount += item.producto.precio_actual * item.cantidad

        data= {
        'cantidad': carrito_item.cantidad,
        'amount': amount,
        'total': amount + 200
      }

      return jsonify(data)
   

@views.route('removecart')
@login_required
def remove_cart():
   if request.method == 'GET':
      carrito_id = request.args.get('carrito_id')
      carrito_item = Carrito.query.get(carrito_id)
      db.session.delete(carrito_item)
      db.session.commit()

      carrito = Carrito.query.filter_by(cliente_link=current_user.id).all()

      amount = 0

      for item in carrito:
        amount += item.producto.precio_actual * item.cantidad

        data= {
        'cantidad': carrito_item.cantidad,
        'amount': amount,
        'total': amount + 200
        }
        
      return jsonify(data)
   





@views.route('/place-order')
@login_required
def place_order():
    cliente_carrito = Carrito.query.filter_by(cliente_link=current_user.id).all()

    if not cliente_carrito:
        flash('Tu carrito está vacío')
        return redirect('/')

    try:
        total = 0

        # Verificar stock antes de hacer cualquier cambio
        for item in cliente_carrito:
            producto = Producto.query.get(item.producto_link)
            if not producto:
                flash(f'Producto con ID {item.producto_link} no encontrado')
                return redirect('/')
            if producto.en_stock < item.cantidad:
                flash(f"No hay suficiente stock de '{producto.nombre_producto}'")
                return redirect('/')

        # Crear órdenes, actualizar stock, y limpiar carrito
        for item in cliente_carrito:
            producto = Producto.query.get(item.producto_link)

            nueva_orden = Orden(
                cantidad=item.cantidad,
                precio=producto.precio_actual,
                producto_link=item.producto_link,
                cliente_link=item.cliente_link,
                status='pendiente',
                payment_id='manual-test'  
            )

            db.session.add(nueva_orden)

            producto.en_stock -= item.cantidad
            db.session.delete(item)

            total += producto.precio_actual * item.cantidad

        db.session.commit()
        flash('Orden realizada exitosamente')
        print(f'Orden colocada por el cliente {current_user.id}. Total: ${total:.2f}')
        return redirect('/ordenes')

    except Exception as e:
        db.session.rollback()  # Revierte todos los cambios en caso de error
        print("Error al procesar la orden:", e)
        traceback.print_exc()
        flash('Orden no realizada por un error interno')
        return redirect('/')


@views.route('/ordenes')
@login_required
def orden():
   ordenes = Orden.query.filter_by(cliente_link=current_user.id).all()
   return render_template('orders.html', ordenes=ordenes)




@views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('Search')
        items = Producto.query.filter(Producto.nombre_producto.ilike(f'%{search_query}%')).all()
        return render_template(
            'search.html',
            items=items,
            carrito=Carrito.query.filter_by(cliente_link=current_user.id).all() if current_user.is_authenticated else []
        )
    
    # GET request: no hay búsqueda, pero igual pasamos items vacío
    return render_template(
        'search.html',
        items=[],
        carrito=Carrito.query.filter_by(cliente_link=current_user.id).all() if current_user.is_authenticated else []
    )



      
         
      



      
      




