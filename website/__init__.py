from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
 #DB_NAME = 'database.sqlite3'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'esto es una cadena de caracteres'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin1234@127.0.0.1:3307/Shopix'



    db.init_app(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html')

    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'


    @login_manager.user_loader
    def load_user(id):
        return Cliente.query.get(int(id))


    # Importa las rutas (blueprints)
    from .views import views
    from .auth import auth
    from .admin import admin

    # Registra los blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth)
    app.register_blueprint(admin, url_prefix='/')

    # Importa los modelos para que SQLAlchemy los conozca
    from .models import Cliente, Producto, Carrito, Orden

    # Crea la base de datos si no existe
    #create_database(app)

    # Devuelve la instancia de la app al final
    return app

#def create_database(app):
    #if not path.exists(DB_NAME):
        #with app.app_context():
            #db.create_all()
            #print(' Base de datos creada.')
    #else:
        #print('ℹBase de datos ya existe.')

