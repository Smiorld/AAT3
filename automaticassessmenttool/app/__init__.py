from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from flask_ckeditor import CKEditor

app = Flask(__name__)
# add ckeditor for rich text fields
ckeditor = CKEditor(app)

app.config["SECRET_KEY"] = "CHANGEME"

# suppress SQLAlchemy warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "aat.db")

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from app import routes
