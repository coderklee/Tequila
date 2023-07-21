from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow
import secrets

# set variables for class instantiation

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String, nullable=True, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, default='', unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, first_name='', last_name='', email='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f"User {self.email} has been added to the database."
    
    
class Tequila(db.Model):
    id = db.Column(db.String, primary_key=True)
    brand = db.Column(db.String(100))
    color = db.Column(db.String(100))
    region = db.Column(db.String(100))
    alcohol = db.Column(db.String(10))
    price = db.Column(db.String(10))
    user_token = db.Column(db.ForeignKey('user.token'), nullable=False)

    def __init__(self, brand, color, region, alcohol, price, user_token, id=''):
        self.id = self.set_id()
        self.brand = brand
        self.color = color
        self.region = region
        self.alcohol = alcohol
        self.price = price
        self.user_token = user_token
        
    def __repr__(self):
        return f"The following tequila has been added to the database: {self.brand}"
    
    def set_id(self):
        return(secrets.token_urlsafe())
    
class TequilaSchema(ma.Schema):
    class Meta:
        fields = ['id', 'brand', 'color' 'region', 'alcohol', 'price']

tequila_schema = TequilaSchema()
tequilas_schema = TequilaSchema(many=True)