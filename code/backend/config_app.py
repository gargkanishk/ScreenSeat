#import flask
from flask import Flask
#import flask_cors
from flask_cors import CORS
#import os
import os

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret_key'

#debug mode
app.config['DEBUG'] = True

#cors
CORS(app)

app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'b47d416f6186f0'
app.config['MAIL_PASSWORD'] = '192651e4e08bec'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

app.config['DEBUG'] = True

current_dir = os.path.abspath(os.path.dirname (__file__) )
app.config [ 'SQLALCHEMY_DATABASE_URI' ] = "sqlite:///" + os.path.join(current_dir , "database.db")
app.config [ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False


