from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json

from config import redis_client

app = Flask(__name__)
app.config.from_object(str(redis_client.get('APP_SETTINGS').decode('utf-8')))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



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
        new_member = Members(phone_number=phone_number, \
        first_name=first_name, last_name=last_name)
        db.session.add(new_member)
        db.session.commit()

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)
