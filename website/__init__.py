from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_socketio import SocketIO

# The db object is defined here
db = SQLAlchemy()
DB_NAME = "database.db"
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret_key'

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # The db object is initialized with the app here
    db.init_app(app)
    
    socketio.init_app(app) 

    # Import the models here, after the db object has been initialized
    from .models import User 

    from .views import views
    from .auth import auth
    from .site import site 
    from .profile import profile 
    from .admin import admin
    from .chat import chat

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/authentification')
    app.register_blueprint(site, url_prefix='/dashboard')
    app.register_blueprint(profile, url_prefix='/profile')
    app.register_blueprint(admin, url_prefix='/admin') 
    app.register_blueprint(chat, url_prefix='/chat')

    # It is good practice to call create_database within the app_context
    with app.app_context():
        create_database()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database():
    # Use path.exists on a relative path to the project root
    if not path.exists('website/' + DB_NAME):
        db.create_all()
        print('Created Database!')
    