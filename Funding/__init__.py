from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///funding.db'
app.config['SECRET_KEY']='e02fb8dc6d8a4b29cd4ad808'

app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '2181715@dut4life.ac.za'
app.config['MAIL_PASSWORD'] = 'Dut9907722'
app.config['MAIL_DEFAULT_SENDER'] = '2181715@dut4life.ac.za'

mail = Mail(app)

with app.app_context():
    mail.init_app(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager= LoginManager(app)
csrf = CSRFProtect(app)
from Funding import routes
