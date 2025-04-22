from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, length, NumberRange
from flask_wtf.file import FileField, FileRequired

class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), length(min=2)])
    password1 = PasswordField('Ingresa tu contraseña', validators=[DataRequired(), length(min=6)])
    password2 = PasswordField('Confirma tu contraseña', validators=[DataRequired(),length(min=6)])
    submit = SubmitField('Registrate')



class LoginForm(FlaskForm):
    email =EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Ingresa tu contraseña', validators=[DataRequired()])
    submit = SubmitField('Inicia Sesión')


class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Contraseña actual', validators=[DataRequired(), length(min=6)])
    new_password = PasswordField('Contraseña nueva', validators=[DataRequired(), length(min=6)])
    confirm_new_password = PasswordField('Confirma la nueva contraseña', validators=[DataRequired(), length(min=6)])
    change_password = SubmitField('Cambiar contraseña')


class ShopItemsForm(FlaskForm):
    nombre_producto = StringField('Nombre del producto', validators=[DataRequired()])
    precio_actual = FloatField('Precio actual', validators=[DataRequired()])
    precio_previo = FloatField('Precio previo', validators=[DataRequired()])
    en_stock = IntegerField('En stock', validators=[DataRequired(), NumberRange(min=0)])
    imagen_producto = FileField ('Imagen del producto', validators=[FileRequired()])
    flash_sale = BooleanField('Flash Sale')


    agregar_producto = SubmitField('Agregar Producto')
    actualizar_producto = SubmitField('Actualizar')



class OrderForm(FlaskForm):
    orden_status = SelectField('Orden Status', choices=[('Pendiente', 'Pendiente'), ('Aceptada', 'Aceptada'),
                                                        ('fuera de entrega', 'fuera de entrega'),
                                                        ('Entregado', 'Entregado'), ('Cancelado', 'Cancelado')])

    update = SubmitField('Actualizar Status')