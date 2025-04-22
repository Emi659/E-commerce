from . import db 
from flask_login import UserMixin
from datetime import datetime 
from werkzeug.security import generate_password_hash, check_password_hash

class Cliente(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String(256))
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)

    carrito_items = db.relationship('Carrito', backref=db.backref('cliente', lazy=True))
    ordenes = db.relationship('Orden', backref=db.backref('cliente', lazy=True))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password=password) 

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password=password)

    def __str__(self):
        return f'<Cliente {self.id}>'

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_producto = db.Column(db.String(100), nullable=False)
    precio_actual = db.Column(db.Float, nullable=False)
    precio_previo = db.Column(db.Float, nullable=False)
    en_stock = db.Column(db.Integer, nullable=False)
    imagen_producto = db.Column(db.String(1000), nullable=False)
    flash_sale = db.Column(db.Boolean, default=False)
    fecha_agregacion = db.Column(db.DateTime, default=datetime.utcnow)

    carritos = db.relationship('Carrito', backref=db.backref('producto', lazy=True))
    ordenes = db.relationship('Orden', backref=db.backref('producto', lazy=True))

    def __str__(self):
        return f'<Producto {self.nombre_producto}>'

class Carrito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    cliente_link = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    producto_link = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)

    def __str__(self):
        return f'<Carrito {self.id}>'

class Orden(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    cliente_link = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    producto_link = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pendiente') 
    payment_id = db.Column(db.String(100), nullable=False)


    def __str__(self):
        return f'<Orden {self.id}>'


            

    
