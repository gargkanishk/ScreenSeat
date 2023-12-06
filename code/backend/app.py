import base64
import json
import os
from io import BytesIO
from flask import Flask, flash, make_response, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import matplotlib.pyplot as plt
from flask import jsonify, request
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask_mail import Mail
import redis
from rq import Queue
from apscheduler.schedulers.background import BackgroundScheduler
from flask_mail import Message
from celery.result import AsyncResult
from celery.schedules import crontab
from worker_celery import create_celery_app
from models import User, Booking, Show, Venue
import celery_tasks
from config_app import app
from models import db


r = redis.Redis()
q = Queue(connection=r)
scheduler = BackgroundScheduler(daemon=True)

cel_app = create_celery_app(app)

@cel_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        20,
        celery_tasks.send_email.s()
    )

    sender.add_periodic_task(
        20,
        celery_tasks.monthly_progress_report.s()
    )

    sender.add_periodic_task(
        10.0,
        celery_tasks.test.s()
    )





#schedule email
#scheduler.add_job(func=send_email, trigger="interval", minutes=1)

#scheduler.start()



#schedule monthly progress report that is triggered on the first day of every month
#scheduler.add_job(func=monthly_progress_report, trigger="interval", minutes=1)

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

SECRET_KEY = 'your_secret_key_here'

@app.route('/api/check_auth')
def check_auth():
    if current_user.is_authenticated:  
        return jsonify({'authenticated': True})
    else:
        return jsonify({'authenticated': False}), 401

# Create a route to home page
@app.route('/')
def index():
    #redirect to user login page
    return redirect(url_for('user_login'))


#one time route for adding admin user
#@app.route('/add_admin')
#def add_admin():
#    user = User.query.filter_by(username='admin').first()
#    if user:
#        return 'Admin user already exists!'
#    else:
#        new_user = User(username='admin', password=generate_password_hash('admin', method='sha256'))
#        db.session.add(new_user)
#        db.session.commit()
#        return 'Admin user created!'


def auth_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        # Check if the Authorization header is present in the request
        if 'Authorization' in request.headers:
            # Get the token from the Authorization header
            auth_header = request.headers['Authorization']
            token = auth_header.split(' ')[1]

        if not token:
            # If token is missing, return an error response
            return jsonify({'message': 'Authentication token is missing.', 'authenticated': False}), 401

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired.', 'authenticated': False}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token.', 'authenticated': False}), 401

        # If authentication is successful, proceed with the original function
        return func(*args, **kwargs)

    return decorated


# logout route
@app.route('/api/logout')
@auth_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful!', 'authenticated': False}), 200

#user login route
@app.route('/api/user_login', methods=['POST'])
def user_login():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.isAdmin==0 and check_password_hash(user.password, password):
            login_user(user)
            global current_user
            current_user = user

            token_payload = {
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(hours=1)
            }

            token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')

            return make_response(jsonify({'message': 'Login successful!', 'login': True, 'token': token, 'token_payload': token_payload}), 200)
        else:
            flash('Invalid username or password!')
            return make_response(jsonify({'message': 'Invalid username or password!', 'login': False, 'success': False}), 401)
    else:
        return make_response(jsonify({'message': 'Login unsuccessful!', 'login': False, 'success': False}), 401)
    

# Login route
@app.route('/api/admin_login', methods=['POST'])
def admin_login():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.isAdmin==1 and check_password_hash(user.password, password):
            login_user(user)    
            global current_user
            current_user = user

            token_payload = {
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(hours=1)
            }

            token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')

            return make_response(jsonify({'message': 'Login successful!', 'login': True, 'success': True, 'token': token, 'token_payload': token_payload}), 200)
        else:
            flash('Invalid username or password!')
            return make_response(jsonify({'message': 'Invalid username or password!', 'login': False, 'success': False}), 401)
    else:
        return make_response(jsonify({'message': 'Login unsuccessful!', 'login': False, 'success': False}), 401)


#user signup route
@app.route('/api/user_signup', methods=['POST'])
def user_signup():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        if '@' not in username:
            flash('Invalid email!')
            return make_response(jsonify({'message': 'Invalid email!', 'signup': False}), 409)
        
        print("#######################")
        print(username, password)
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username or email already exists!')
            return make_response(jsonify({'message': 'Username or email already exists!', 'signup': False}), 409)

        # create new user
        new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash('Account created!')
        print("Account created!")
        return make_response(jsonify({'message': 'Account created!', 'signup': True}), 201)

    else:
        print("Signup unsuccessful!")
        return make_response(jsonify({'message': 'Signup unsuccessful!', 'signup': False}), 409)

@app.route('/api/user_dashboard')
@auth_required
def user_dashboard():
    venues = Venue.query.all()
    data = []
    
    for venue in venues:
        venue_data = {
            'id': venue.id,
            'venue_name': venue.venue_name,
            'venue_location': venue.venue_location,
            'venue_capacity': venue.venue_capacity,
            'venue_description': venue.venue_description,
            'shows': []
        }

        for show in venue.shows:
            show_data = {
                'id': show.id,
                'show_name': show.show_name,
                'show_date': show.show_date,
                'show_time': show.show_time,
                'show_price': show.show_price
            }
            venue_data['shows'].append(show_data)

        data.append(venue_data)

    return jsonify({'message': 'User dashboard!', 'success': True, 'data': data})




        

#book show route
@app.route('/api/book_show/<int:show_id>', methods=['GET', 'POST'])
@auth_required
def book_show(show_id):
    show = Show.query.get(show_id)
    venue = Venue.query.get(show.venue_id)
    user = User.query.get(current_user.id)
    if request.method == 'POST':
        tickets = request.json.get('tickets')
        total_price = int(tickets) * int(show.show_price)
        new_booking = Booking(show_id=show_id, user_id=current_user.id, tickets=tickets, total_price=total_price)
        show.show_available_tickets = int(show.show_available_tickets) - int(tickets)
        db.session.add(new_booking)
        db.session.commit()
        flash('Booking successful!')
        return make_response(jsonify({'message': 'Booking successful!', 'success': True}), 201)
    
    data = {
        'show': {
            'id': show.id,
            'show_name': show.show_name,
            'show_date': show.show_date,
            'show_time': show.show_time,
            'show_price': show.show_price,
            'tags': show.show_tags,
            'capacity': show.show_capacity,
            'show_available_tickets': show.show_available_tickets,
            'venue_id': show.venue_id
        },
        'venue': {
            'id': venue.id,
            'name': venue.venue_name,
            'location': venue.venue_location,
            'capacity': venue.venue_capacity,
            'description': venue.venue_description
        },
        'user': {
            'id': user.id,
            'username': user.username
        }
    }
    return jsonify({'message': 'Booking page!', 'success': True, 'data': data})

# search venue route
@app.route('/api/search/', methods=['POST'])
@auth_required
def search():
    if request.method == 'POST':
        if request.json['search_selector'] == 'venue':
            search_term = request.json['search_term']
            search_term = search_term.lower()
            venues = Venue.query.filter(or_(Venue.venue_name.ilike('%' + search_term + '%'), Venue.venue_location.ilike('%' + search_term + '%'))).all()
            data = []
            for venue in venues:
                venue_data = {
                    'id': venue.id,
                    'venue_name': venue.venue_name,
                    'venue_location': venue.venue_location,
                    'venue_capacity': venue.venue_capacity,
                    'venue_description': venue.venue_description,
                }

                data.append(venue_data)
            
            return jsonify({'message': 'Search Results', 'success': True, 'data': data}), 200

        else:
            # Handle show search logic here if needed
            show_name = request.json['search_term']
            show_name = show_name.lower()
            shows = Show.query.filter(Show.show_name.ilike('%' + show_name + '%')).all()
            data = []
            for show in shows:
                show_data = {
                    'id': show.id,
                    'show_name': show.show_name,
                    'show_date': show.show_date,
                    'show_time': show.show_time,
                    'show_price': show.show_price,
                    'tags': show.show_tags,
                    'capacity': show.show_capacity,
                    'show_available_tickets': show.show_available_tickets,
                    'venue_id': show.venue_id
                }
                # Get the venue details for the show
                venue = Venue.query.get(show.venue_id)
                show_data['venue_name'] = venue.venue_name
                show_data['venue_location'] = venue.venue_location

                data.append(show_data)
            return jsonify({'message': 'Search Results', 'success': True, 'data': data}), 200
        
#route to display venue and shows for a venue
@app.route('/api/venue_details/<venue_id>')
def venue(venue_id):
    venue = Venue.query.get(venue_id)
    shows = Show.query.filter_by(venue_id=venue_id).all()
    data = {
        'venue': {
            'id': venue.id,
            'venue_name': venue.venue_name,
            'venue_location': venue.venue_location,
            'venue_capacity': venue.venue_capacity,
            'venue_description': venue.venue_description,
            'shows': []
        }
    }

    for show in shows:
        show_data = {
            'id': show.id,
            'show_name': show.show_name,
            'show_date': show.show_date,
            'show_time': show.show_time,
            'show_price': show.show_price,
            'tags': show.show_tags,
            'capacity': show.show_capacity,
            'show_available_tickets': show.show_available_tickets,
            'venue_id': show.venue_id

        }
        data['venue']['shows'].append(show_data)

    return make_response(jsonify({'message': 'Venue page!', 'success': True, 'data': data}), 200)

#bookings route
@app.route('/api/my_bookings/<user_id>')
def bookings(user_id):
    bookings = Booking.query.filter_by(user_id=user_id).all()
    data = []
    for booking in bookings:
        show = Show.query.get(booking.show_id)
        venue = Venue.query.get(show.venue_id)
        booking_data = {
            'id': booking.id,
            'tickets': booking.tickets,
            'total_price': booking.total_price,
            'show_id': booking.show_id,
            'user_id': booking.user_id,
            'show_rating': booking.show_rating,
            'show_name': show.show_name,
            'show_date': show.show_date,
            'show_time': show.show_time,
            'show_price': show.show_price,
            'show_tags': show.show_tags,
            'show_capacity': show.show_capacity,
            'show_available_tickets': show.show_available_tickets,
            'venue_id': venue.id,
            'venue_name': venue.venue_name,
            'venue_location': venue.venue_location,
            'venue_capacity': venue.venue_capacity,
            'venue_description': venue.venue_description
        }
        data.append(booking_data)

    return make_response(jsonify({'message': 'Bookings page!', 'success': True, 'data': data}), 200)
    
    
#rate show route
@app.route('/api/rate_show/<booking_id>', methods=['POST'])
def rate_show(booking_id):
    booking = Booking.query.get(booking_id)
    show_id = booking.show_id
    show = Show.query.get(show_id)
    if request.method == 'POST':
        show_rating = request.json.get('show_rating')
        current_rating = show.show_rating
        booking.show_rating = show_rating
        if show.show_rating_count == 0:
            new_rating = show_rating
        else:


            new_rating = (float(current_rating) + float(show_rating)) / 2
        
        show.show_rating_count += 1
        show.show_rating = new_rating
        db.session.commit()
        flash('Show rated!')

        return make_response(jsonify({'message': 'Show rated!', 'success': True}), 201)
    
#all venues and shows
@app.route('/api/admin_dashboard')
@auth_required
def all_venues():
    venues = Venue.query.all()
    data = []
    for venue in venues:
        venue_data = {
            'id': venue.id,
            'venue_name': venue.venue_name,
            'venue_location': venue.venue_location,
            'venue_capacity': venue.venue_capacity,
            'venue_description': venue.venue_description,
            'shows': []
        }

        for show in venue.shows:
            show_data = {
                'id': show.id,
                'show_name': show.show_name,
                'show_date': show.show_date,
                'show_time': show.show_time,
                'show_price': show.show_price,
                'tags': show.show_tags,
                'capacity': show.show_capacity,
                'show_available_tickets': show.show_available_tickets,
                'venue_id': show.venue_id
            }
            venue_data['shows'].append(show_data)

        data.append(venue_data)

    return jsonify({'message': 'All venues!', 'success': True, 'data': data})


#create venue route
@app.route('/api/create_venue', methods=['POST'])
@auth_required
def create_venue():
    data = request.json
    venue_name = data.get('venue_name')
    venue_description = data.get('venue_description')
    venue_location = data.get('venue_location')
    venue_capacity = data.get('venue_capacity')
    existing_venue = Venue.query.filter_by(venue_name=venue_name).first()
    if existing_venue:
        return jsonify({'message': 'Venue already exists!'}), 409
    
    if not venue_name or not venue_description or not venue_location or not venue_capacity:
        return jsonify({'message': 'All fields are required!'}), 409
    
    if len(venue_name) < 3 or len(venue_name) > 50:
        return jsonify({'message': 'Venue name must be between 3 and 50 characters!'}), 409
    
    if len(venue_description) < 3 or len(venue_description) > 500:
        return jsonify({'message': 'Venue description must be between 3 and 500 characters!'}), 409
    
    if len(venue_location) < 3 or len(venue_location) > 50:
        return jsonify({'message': 'Venue location must be between 3 and 50 characters!'}), 409
    
    if int(venue_capacity) < 1 or int(venue_capacity) > 100000:
        return jsonify({'message': 'Venue capacity must be between 1 and 100000!'}), 409

    new_venue = Venue(
        venue_name=venue_name, 
        venue_description=venue_description, 
        venue_location=venue_location, 
        venue_capacity=venue_capacity
    )
    db.session.add(new_venue)
    db.session.commit()

    return jsonify({'message': 'Venue created!', 'success': True}), 201


#edit venue route
@app.route('/api/update_venue/<venue_id>', methods=['POST'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    if request.method == 'POST':
        venue_name = request.json.get('venue_name')
        venue_description = request.json.get('venue_description')
        venue_location = request.json.get('venue_location')
        venue_capacity = request.json.get('venue_capacity')
        existing_venue = Venue.query.filter_by(venue_name=venue_name).first()
        if existing_venue:
            return jsonify({'message': 'Venue already exists!'}), 409
        
        #validate all fields
        if not venue_name or not venue_description or not venue_location or not venue_capacity:
            return jsonify({'message': 'All fields are required!'}), 409
        
        if len(venue_name) < 3 or len(venue_name) > 50:
            return jsonify({'message': 'Venue name must be between 3 and 50 characters!'}), 409
        
        if len(venue_description) < 3 or len(venue_description) > 5000:
            return jsonify({'message': 'Venue description must be between 3 and 5000 characters!'}), 409
        
        if len(venue_location) < 3 or len(venue_location) > 500:
            return jsonify({'message': 'Venue location must be between 3 and 500 characters!'}), 409
        
        if int(venue_capacity) < 1 or int(venue_capacity) > 100000:
            return jsonify({'message': 'Venue capacity must be between 1 and 100000!'}), 409

        venue.venue_name = venue_name
        venue.venue_description = venue_description
        venue.venue_location = venue_location
        venue.venue_capacity = venue_capacity
        db.session.commit()
        flash('Venue updated!')
        return jsonify({'message': 'Venue updated!', 'success': True}), 201


#delete venue route
@app.route('/api/delete_venue/<venue_id>', methods=['GET', 'POST'])
def delete_venue(venue_id):
    shows = Show.query.filter_by(venue_id=venue_id).all()
    for show in shows:
        bookings = Booking.query.filter_by(show_id=show.id).all()
        for booking in bookings:
            db.session.delete(booking)
            db.session.commit()
        
        db.session.delete(show)
        db.session.commit()

    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
    flash('Venue deleted!')
    return jsonify({'message': 'Venue deleted!', 'success': True}), 201

#create show route
@app.route('/api/create_show/<venue_id>', methods=['POST'])
def create_show(venue_id):
    venue = Venue.query.get(venue_id)
    if request.method == 'POST':
        show_name = request.json.get('show_name')
        show_rating = request.json.get('show_rating')
        show_date = request.json.get('show_date')
        show_time = request.json.get('show_time')
        show_price = request.json.get('show_price')
        show_tags = request.json.get('show_tags')
        show_capacity = request.json.get('show_capacity')
        show_available_tickets = request.json.get('show_capacity')
        existing_show = Show.query.filter_by(show_name=show_name).first()
        if existing_show:
            return jsonify({'message': 'Show already exists!'}), 409
        
        #validate all fields
        if not show_name or not show_date or not show_time or not show_price or not show_tags or not show_capacity:
            return jsonify({'message': 'All fields are required!'}), 409
        
        if len(show_name) < 3 or len(show_name) > 500:
            return jsonify({'message': 'Show name must be between 3 and 500 characters!'}), 409
    
        
        if int(show_price) < 1 or int(show_price) > 100000:
            return jsonify({'message': 'Show price must be between 1 and 100000!'}), 409
        
        if len(show_tags) < 3 or len(show_tags) > 500:
            return jsonify({'message': 'Show tags must be between 3 and 500 characters!'}), 409
        
        if int(show_capacity) < 1 or int(show_capacity) > 100000:
            return jsonify({'message': 'Show capacity must be between 1 and 100000!'}), 409
        
        if int(show_available_tickets) < 1 or int(show_available_tickets) > 100000:
            return jsonify({'message': 'Show available tickets must be between 1 and 100000!'}), 409
        
        new_show = Show(
            show_name=show_name,
            show_rating=0,
            show_rating_count=0,
            show_date=show_date,
            show_time=show_time,
            show_price=show_price,
            show_tags=show_tags,
            show_capacity=show_capacity,
            show_available_tickets=show_capacity,
            venue_id=venue_id
        )

        db.session.add(new_show)
        db.session.commit()
        flash('Show created!')
        return jsonify({'message': 'Show created!', 'success': True}), 201
    
#get show details route
@app.route('/api/show_details/<show_id>')
def show_details(show_id):
    show = Show.query.get(show_id)
    venue = Venue.query.get(show.venue_id)
    data = {
        'show': {
            'id': show.id,
            'show_name': show.show_name,
            'show_rating': show.show_rating,
            'show_rating_count': show.show_rating_count,
            'show_date': show.show_date,
            'show_time': show.show_time,
            'show_price': show.show_price,
            'show_tags': show.show_tags,
            'show_capacity': show.show_capacity,
            'show_available_tickets': show.show_available_tickets,
            'venue_id': venue.id,
            'venue_name': venue.venue_name,
            'venue_location': venue.venue_location,
            'venue_capacity': venue.venue_capacity,
            'venue_description': venue.venue_description
        }
    }
    return jsonify({'message': 'Show details!', 'success': True, 'data': data}), 200
    
#edit show route
@app.route('/api/edit_show/<show_id>', methods=['POST'])
def edit_show(show_id):
    show = Show.query.get(show_id)
    venue = Venue.query.get(show.venue_id)
    if request.method == 'POST':
        show_name = request.json.get('show_name')
        show_date = request.json.get('show_date')
        show_time = request.json.get('show_time')
        show_price = request.json.get('show_price')
        show_tags = request.json.get('show_tags')
        existing_show = Show.query.filter_by(show_name=show_name).first()
        if existing_show:
            return jsonify({'message': 'Show already exists!'}), 409
        
        if not show_name or not show_date or not show_time or not show_price or not show_tags:
            return jsonify({'message': 'All fields are required!'}), 409
        
        if len(show_name) < 3 or len(show_name) > 500:
            return jsonify({'message': 'Show name must be between 3 and 500 characters!'}), 409
    
        
        if int(show_price) < 1 or int(show_price) > 100000:
            return jsonify({'message': 'Show price must be between 1 and 100000!'}), 409
        
        if len(show_tags) < 3 or len(show_tags) > 500:
            return jsonify({'message': 'Show tags must be between 3 and 500 characters!'}), 409
        
        show.show_name = show_name
        show.show_date = show_date
        show.show_time = show_time
        show.show_price = show_price
        show.show_tags = show_tags
        db.session.commit()
        flash('Show updated!')
        return jsonify({'message': 'Show updated!', 'success': True}), 201
    

#delete show route
@app.route('/api/delete_show/<show_id>', methods=['GET', 'POST'])
def delete_show(show_id):
    show = Show.query.get(show_id)
    bookings = Booking.query.filter_by(show_id=show_id).all()
    for booking in bookings:
        db.session.delete(booking)

    db.session.delete(show)
    db.session.commit()
    flash('Show deleted!')
    return jsonify({'message': 'Show deleted!', 'success': True}), 201

#summay graph route
@app.route('/api/summary')
def summary_graph():
    shows = Show.query.all()
    
    show_bookings = {}
    for show in shows:
        bookings = show.bookings
        show_bookings[show] = bookings

    all_show_info = {}

    all_show_info['show_name'] = []
    all_show_info['total_bookings'] = []
    all_show_info['avg_rating'] = []
    all_show_info['total_revenue'] = []
    all_show_info['total_tickets'] = []
    all_show_info['avg_ticket_price'] = []
    all_show_info['avg_tickets_per_booking'] = []


    for show, bookings in show_bookings.items():
        all_show_info['total_bookings'].append(len(bookings))
        all_show_info['show_name'].append(show.show_name)
        all_show_info['avg_rating'].append(float(show.show_rating))
        all_show_info['total_tickets'].append(float(show.show_capacity) - float(show.show_available_tickets))
        total_revenue = 0
        count_tickets = 0
        for booking in bookings:
            total_revenue += int(booking.total_price)
            count_tickets += int(booking.tickets)

        all_show_info['total_revenue'].append(total_revenue)
        if len(bookings) == 0:
            all_show_info['avg_ticket_price'].append(total_revenue)
            all_show_info['avg_tickets_per_booking'].append(count_tickets)
        else:
            all_show_info['avg_ticket_price'].append(total_revenue/len(bookings))
            all_show_info['avg_tickets_per_booking'].append(count_tickets/len(bookings))

    df = pd.DataFrame(all_show_info)

    df.to_csv('../ticket_booking/src/assets/summary_graph.csv', index=False)

    fig, axs = plt.subplots(nrows=df.shape[0], figsize=(6, 4*df.shape[0]))


    for i, (index, row) in enumerate(df.iterrows()):
        col_title = row[0]  
        x_labels = list(row.index)[1:] 
        x_values = row.values[1:] 

        plt.setp(axs[i].get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")


        for j, v in enumerate(x_values):
            axs[i].text(j, v, str(v), color='blue', fontweight='bold')
    
        axs[i].bar(x_labels, x_values)
        axs[i].set_title(col_title)

    fig.tight_layout()
    
    fig.savefig('../ticket_booking/src/assets/summary_graph.png')

    return jsonify({'message': 'Summary graph created!', 'success': True}), 201

# route to display ratings for each show
@app.route('/show_ratings')
@login_required
def show_ratings():
    shows = Show.query.all()
    ratings = {}
    for show in shows:
        show_ratings = show.get_ratings()
        for rating, count in show_ratings.items():
            if rating in ratings:
                ratings[rating] += count
            else:
                ratings[rating] = count
    return render_template('show_ratings.html', page_title='Show Ratings', ratings=ratings)



if __name__ == '__main__':
    app.run()
