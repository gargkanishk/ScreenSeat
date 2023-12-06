from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from config_app import app
#import db
db = SQLAlchemy(app)

#User class
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    isAdmin = db.Column(db.Integer, default=0)

#venue class
class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_name = db.Column(db.String(50), unique=True)
    venue_description = db.Column(db.String(50))
    venue_location = db.Column(db.String(50))
    venue_capacity = db.Column(db.String(50))
    shows = db.relationship('Show', backref='venue', lazy=True)

#show class
class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    show_name = db.Column(db.String(50))
    show_rating = db.Column(db.String(50))
    show_rating_count = db.Column(db.Integer)
    show_date = db.Column(db.String(50))
    show_time = db.Column(db.String(50))
    show_price = db.Column(db.String(50))
    show_tags = db.Column(db.String(50))
    show_capacity = db.Column(db.Integer)
    show_available_tickets = db.Column(db.Integer)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    bookings = db.relationship('Booking', backref='show', lazy=True)

#booking class
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tickets = db.Column(db.Integer)
    total_price = db.Column(db.Integer)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    show_rating = db.Column(db.Integer)