from flask import Flask
from flask_mail import Mail, Message
#import crontab
from celery.schedules import crontab
#import models
from models import User, Booking, Show, Venue
import pandas as pd
import logging
from config_app import app
from celery import shared_task
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
#import mail from app

mail = Mail(app)

#function to schedule email
@shared_task(ignore_result=False)
def send_email():
    users = User.query.all()
    recipients = []
    for user in users:
        bookings = Booking.query.filter_by(user_id=user.id).all()
        if len(bookings) == 0:
            if '@' in user.username:
                recipients.append(user.username)
    if recipients == []:
        print("No users to send email to!")
        return
    msg = Message('Hello', sender = 'infogargkanishk@gmail.com' , recipients = recipients)
    msg.body = "Please make a booking"
    mail.send(msg)
    
#funcitn to schedule monthly progress report and send it as email
@shared_task(ignore_result=False)
def monthly_progress_report():
    shows = Show.query.all()
    data = []
    for show in shows:
        bookings = Booking.query.filter_by(show_id=show.id).all()
        total_tickets_booked = 0
        for booking in bookings:
            total_tickets_booked += booking.tickets
        venue = Venue.query.get(show.venue_id)
        show_date = show.show_date
        show_rating = show.show_rating
        venue_capacity = venue.venue_capacity
        percentage_tickets_booked = (total_tickets_booked / venue_capacity) * 100
        total_tickets_available = venue_capacity - total_tickets_booked
        info = {
            'show_name': [show.show_name],
            'show_date': [show.show_date],
            'show_time': [show.show_time],
            'show_price': [show.show_price],
            'venue_capacity': [venue_capacity],
            'total_tickets_booked': [total_tickets_booked],
            'percentage_tickets_booked': [percentage_tickets_booked],
            'total_tickets_available': [total_tickets_available],
            'venue_name': [venue.venue_name],
        }
        #add the data to the data list
        data.append(info)
    df = pd.DataFrame(data)
    df.to_csv('monthly_progress_report.csv', index=False)
    with app.open_resource("monthly_progress_report.csv") as fp:
        msg = Message(
            "Monthly Progress Report",
            sender="infogargkanishk@gmail.com",
            recipients=["infogargkanishk@gmail.com"],
            body="Please find the monthly progress report attached."
        )
        msg.attach(
            "monthly_progress_report.csv",
            "text/csv",
            fp.read()
        )
        mail.send(msg)

@shared_task(ignore_result=False)
def test():
    logger.info("Hello World!")
