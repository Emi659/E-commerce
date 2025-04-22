from flask import Blueprint, render_template, flash, redirect
from .forms import LoginForm, SignUpForm, PasswordChangeForm
from .models import Cliente
from . import db
from flask_login import login_user, login_required, logout_user

auth = Blueprint('auth', __name__)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up ():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data

        if password1 == password2:
            nuevo_cliente = Cliente()
            nuevo_cliente.email = email
            nuevo_cliente.username = username
            nuevo_cliente.password = password2

            try:
                db.session.add(nuevo_cliente)
                db.session.commit()
                flash('Cuenta creada exitosamente, ya puedes iniciar sesión')
                return redirect('/login')
            except Exception as e:
                print(e)
                flash('Cuenta no creada, el email ya existe')

            form.email.data = ''
            form.username.data = ''
            form.password1.data = ''
            form.password2.data = ''

    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login ():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        cliente = Cliente.query.filter_by(email=email).first()

        if cliente:
            if cliente.verify_password(password=password):
                login_user(cliente)
                return redirect('/')
            else:
                flash('Contraseña o correo incorrecto')



        else:
            flash('La cuenta no existe, por favor registrate')
   
    return render_template('login.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def log_out():
   logout_user() 
   return redirect('/')

@auth.route('/profile/<int:cliente_id>')
@login_required
def profile(cliente_id):
    cliente = Cliente.query.get(cliente_id)
    print('Cliente ID:', cliente_id)
    return render_template('profile.html', cliente=cliente)

@auth.route('/change-password/<int:cliente_id>', methods=['GET', 'POST'])
@login_required
def change_password(cliente_id):
    form = PasswordChangeForm()
    cliente = Cliente.query.get(cliente_id)
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_new_password = form.confirm_new_password.data

        if cliente.verify_password(current_password):
            if new_password == confirm_new_password:
                cliente.password = confirm_new_password
                db.session.commit()
                flash('Contraseña actualizada')
                return redirect(f'/profile/{cliente.id}')

        else:
            flash('Contraseña incorrecta')


    return render_template('change_password.html', form=form)