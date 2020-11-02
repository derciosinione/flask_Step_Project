from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '4b5614eae24fa84d1c9e0156f8762149'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbStep.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost:3307/dbStep'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message = "Por favor, efectua o login para acessar a área administrativa."
login_manager.login_message_category = 'info'

from stepsite.main.routes import main 
from stepsite.users.routes import users 
from stepsite.projectos.routes import projects 
from stepsite.entidades.routes import entidads 
from stepsite.categorias.routes import category 

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(projects)
app.register_blueprint(entidads)  
app.register_blueprint(category)  