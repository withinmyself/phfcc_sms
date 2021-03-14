from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json
import schedule_handler
from schedule_handler import AlertScheduler

import smtplib
import redis

import schedule
import time


from config import redis_client

app = Flask(__name__)
app.config.from_object(str(redis_client.get('APP_SETTINGS').decode('utf-8')))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

schedule_obj = AlertScheduler('monday')

# Database models for PostgreSQL and SQLAlchemy
class Members(db.Model):
    __tablename__ = 'phfcc_members'

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String())
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    is_subscriber = db.Column(db.Boolean())

    def __init__(self, phone_number, first_name, last_name, is_subscriber=True):
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.is_subscriber = is_subscriber

    def __repr__(self):
        return f'{self.last_name}, {self.first_name}, {self.phone_number}'

class Messages(db.Model):
    __tablename__ = 'phfcc_messages'

    id = db.Column(db.Integer, primary_key=True)
    message_type = db.Column(db.String())
    message = db.Column(db.String(128))
    auto_send = db.Column(db.Boolean())


    def __init__(self, message_type, message, auto_send=False):
        self.message_type = message_type
        self.message = message
        self.auto_send = auto_send

    def __repr__(self):
        return f'{self.message}'



class SendSMS():
    """
    """
    def __init__(self):
        self._redis_client = redis.Redis()
        self._members_to_text = Members.query.all()
        self._covid_message = Messages.query.filter_by(message_type='Covid').first()
        self._weather_message = Messages.query.filter_by(message_type='Weather').first()
        self._meetings = Messages.query.filter_by(message_type='Meetings').first()
        self._prayer_chain = Messages.query.filter_by(message_type='Prayer Chain').first()
        self._username = str(self._redis_client.get('SMS_USER').decode('utf-8'))
        self._password = str(self._redis_client.get('SMS_PASS').decode('utf-8'))


    def send_sms_all(self, message_type):
        members_to_text = Members.query.all()
        self.message_type = message_type
        for member in members_to_text:
            if message_type == 'ALL':
                self.send_sms(str(member.phone_number), self._covid_message.message)
                self.send_sms(str(member.phone_number), self._weather_message.message)
                self.send_sms(str(member.phone_number), self._meetings.message)
                self.send_sms(str(member.phone_number), self._prayer_chain.message)
                break
                return 'Sent'
            elif message_type == 'Covid':
                self.send_sms(str(member.phone_number), self._covid_message.message)
                return 'Sent'
            elif message_type == 'Weather':
                self.send_sms(str(member.phone_number), self._weather_message.message)
                return 'Sent'
            elif message_type == 'Meetings':
                self.send_sms(str(member.phone_number), self._meetings.message)
                return 'Sent'
            elif message_type == 'Prayer Chain':
                self.send_sms(str(member.phone_number), self._prayer_chain.message)
                return 'Sent'
            else:
                return 'Message Type Not Found.'
        return '200'



    def send_sms(self, number, msg):
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(self._username, self._password)
            from_mail = 'PHFCC'
            to = f'{number}@tmomail.net'
            body = msg
            message = ("From: %s\r\n" % from_mail + "To: %s\r\n" % to + "Subject: %s\r\n" % self.message_type + "\r\n" + body)

            try:
                smtp.sendmail(from_mail, to, message)
            except smtplib.SMTPRecipientsRefused as e:
                print(e)
            return '200'



# Flask routes as API endpoints.

@app.route('/')
def index():
    return 'The Messaging Service for First Christian Church of Pleasant Hill is currently under maintenance.'


@app.route('/change-msg', methods=['GET', 'POST'])
def change_msg():

    request_data = request.args
    message_type = request_data['message_type']
    message = request_data['message']
    current_message = Messages.query.filter_by(message_type=message_type).first()

    try:
        if current_message.message == None:
            pass
    except AttributeError:
        new_message = Messages(message_type, message)
        db.session.add(new_message)
        db.session.commit()
        return ('New Message was added'), 201

    current_message.message = message
    db.session.add(current_message)
    db.session.commit()
    return ('Message was changed'), 201

@app.route('/get-msg', methods=['GET', 'POST'])
def get_msg():
    request_data = request.args
    message_type = request_data['message_type']
    message = Messages.query.filter_by(message_type=message_type).first()

    try:
        check_message = message.message
    except AttributeError:
        return ('There is no message associated with this Message Type.')

    message_dict = {'message_type': message.message_type, \
                         'message': message.message, \
                       'auto-send': message.auto_send}

    return jsonify(message_dict), 200

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    request_data = request.args
    first_name = request_data['first_name']
    last_name = request_data['last_name']
    phone_number = request_data['phone_number']
    check_members = Members.query.filter_by(phone_number=phone_number)

    try:
        if check_members.phone_number != None:
            return (f'The number {check_members.phone_number} is already saved in our system under the name \
                    {check_members.first_name} {check_members.last_name}')


    except AttributeError:
        pass


    new_member = Members(phone_number=phone_number,first_name=first_name, last_name=last_name)

    try:
        db.session.add(new_member)
        db.session.commit()

    except:
        return (f'Phone Number already registered')

    return (f'Thank you {new_member.first_name} {new_member.last_name}. \
            You will start receiving text alerts at {new_member.phone_number}'), 201

@app.route('/change-user', methods=['GET', 'POST'])
def change_user():
    request_data = request.args
    phone_number = request_data['phone_number']
    member = Members.query.filter_by(phone_number=phone_number).first()

    try:
        member.first_name = request_data['new_first_name']
    except KeyError:
        pass

    try:
        member.last_name = request_data['new_last_name']
    except KeyError:
        pass

    try:
        member.phone_number = request_data['new_phone_number']
    except KeyError:
        pass

    db.session.commit()

    members_dict = {'First Name': member.first_name, \
                    'Last Name' : member.last_name, \
                    'Phone Number': member.phone_number}

    return jsonify(members_dict), 201




@app.route('/get-user', methods=['GET', 'POST'])
def get_user():
    request_data = request.args
    phone_number = request_data['phone_number']
    member = Members.query.filter_by(phone_number=phone_number).first()
    member_dict = {'first name': member.first_name, \
                    'last name': member.last_name, \
                 'phone number': member.phone_number}

    return jsonify(member_dict), 200




@app.route('/reports', methods=['GET', 'POST'])
def reports():
    members = Members.query.all()
    if members != None:
        members_dict = {"First Name": [], "Last Name": [], "Phone Number": []};
        for member in members:
            members_dict["First Name"].append(member.first_name)
            members_dict["Last Name"].append(member.last_name)
            members_dict["Phone Number"].append(member.phone_number)
        return jsonify(members_dict), 200
    else:
        return 404



@app.route('/sms', methods=['GET', 'POST'])
def sms():
    request_data = request.args
    sms = SendSMS()
    try:
        sms.send_sms(request_data['number'], request_data['message'])
        return 'Completed', 200
    except KeyError as e:
        pass

    try:
        if request_data['command'] == 'send_all':
            sms.sms_send_all();
            return 200
    except KeyError as e:
        return f'Returned an error -> {e}'

    return 404
@app.route('/stop-scheduler', methods=['GET', 'POST'])
def stop_scheduler():
    schedule_obj.stop_job()
    return 'Stopped', 200










if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)

