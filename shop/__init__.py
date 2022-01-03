from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads
import os
from flask_msearch import Search

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SECRET_KEY']='abc123'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
search = Search()
search.init_app(app)

from shop.admin import routes
from shop.produkty import routes
from shop.koszyk import koszyk