from flask import Blueprint, flash, send_from_directory,redirect
from flask_login import login_required, current_user
from flask import render_template
from .forms import ShopItemsForm,OrderForm
from werkzeug.utils import secure_filename
from .models import Producto, Orden, Cliente
from . import db
import os

admin = Blueprint('admin', __name__)

@admin.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory('../media', filename)

@admin.route('/add-shop-items', methods=['GET', 'POST'])
@login_required
def add_shop_items():
    if current_user.id == 1:
        form = ShopItemsForm()
        
        if form.validate_on_submit():
            nombre_producto = form.nombre_producto.data
            precio_actual = form.precio_actual.data
            precio_anterior = form.precio_previo.data 
            en_stock = form.en_stock.data
            flash_sale = form.flash_sale.data

            file = form.imagen_producto.data

            file_name = secure_filename(file.filename)

            file_path = f'./media/{file_name}'

            file.save(file_path)

           

            new_shop_item = Producto()
            new_shop_item.nombre_producto = nombre_producto
            new_shop_item.precio_actual = precio_actual
            new_shop_item.precio_previo = precio_anterior
            new_shop_item.en_stock = en_stock
            new_shop_item.flash_sale = flash_sale

            new_shop_item.imagen_producto = file_path

            try:
                db.session.add(new_shop_item)
                db.session.commit()
                flash(f'{nombre_producto} agregado exitosamente')
                print('Producto añadido')
                return render_template('add_shop_items.html', form=form)
            except Exception as e:
                print(e)
                flash('Articulo no agregado')
            

        return render_template('add_shop_items.html', form=form)

    return render_template('404.html')


@admin.route('/shop-items', methods=['GET', 'POST'])
@login_required
def shop_items():
    if current_user.id == 1:
      items = Producto.query.order_by(Producto.fecha_agregacion).all()
      return render_template('shop_items.html', items=items)
    return render_template('404.html')


@admin.route('/update-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def actualizar_item(item_id):
    if current_user.id == 1:
        form = ShopItemsForm()

        item_to_update = Producto.query.get(item_id)

        form.nombre_producto.render_kw = {'placeholder': item_to_update.nombre_producto}
        form.precio_previo.render_kw = {'placeholder': item_to_update.precio_previo}
        form.precio_actual.render_kw = {'placeholder': item_to_update.precio_actual}
        form.en_stock.render_kw = {'placeholder': item_to_update.en_stock}
        form.flash_sale_kw = {'placeholder': item_to_update.flash_sale}

        if form.validate_on_submit():
            nombre_producto = form.nombre_producto.data
            precio_actual = form.precio_actual.data
            precio_previo = form.precio_previo.data
            en_stock = form.en_stock.data
            flash_sale = form.flash_sale.data

            file = form.imagen_producto.data

            file_name = secure_filename(file.filename)
            file_path = f'./media/{file_name}'

            file.save(file_path)


            try:
                Producto.query.filter_by(id=item_id).update(dict(nombre_producto=nombre_producto,
                                                                 precio_actual=precio_actual,
                                                                 precio_previo=precio_previo,
                                                                 en_stock=en_stock,
                                                                 flash_sale=flash_sale,
                                                                 imagen_producto=file_path))
                
                db.session.commit()
                flash(f'{nombre_producto} actualizado correctamente')
                print('Producto actualizado')
                return redirect('/shop-items')
            except Exception as e:
                print('Producto no actualizado', e)
                flash('Item no actualizado')
             
            


        
        return render_template('update_item.html', form=form)
     
    return render_template('404.html')

@admin.route('/delete-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    if current_user.id == 1:
        try:
            item_to_delete = Producto.query.get(item_id)
            db.session.delete(item_to_delete)
            db.session.commit()
            flash('Un producto eliminado')
            return redirect('/shop-items')
        except Exception as e:
            print('Item no eliminado', e)
            flash('Item no eliminado')
        return redirect('/shop-items')
    return render_template('404.html')

@admin.route('/view-orders')
@login_required
def order_view():
    if current_user.id == 1:
        ordenes = Orden.query.all()
        return render_template('view_orders.html', ordenes=ordenes)
    return render_template('404.html')




@admin.route('/clientes')
@login_required
def display_cliente():
    if current_user.id == 1:
        clientes = Cliente.query.all()
        return render_template('customers.html', clientes=clientes)
    return render_template('404.html')


@admin.route('/admin-page')
@login_required
def admin_page():
    if current_user.id == 1:
        return render_template('admin.html')
    return render_template ('404.html')

@admin.route('/update-order/<int:orden_id>', methods=['GET', 'POST'])
@login_required
def update_order(orden_id):
    if current_user.id == 1:
        form = OrderForm()

        orden = Orden.query.get(orden_id)

        if form.validate_on_submit():
            status = form.orden_status.data
            orden.status = status

            try:
                db.session.commit()
                flash(f'Orden {orden_id} Actualizada correctamente')
                return redirect('/view-orders')
            except Exception as e:
                print(e)
                flash(f'Orden {orden_id} no actualizada')
                return redirect('/view-orders')


        return render_template('order_update.html', form=form)
    return render_template('404.html')