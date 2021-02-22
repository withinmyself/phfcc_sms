from app import db


class Members(db.Model):
    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.Integer)
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
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    message_type = db.Column(db.String())
    message = db.Column(db.String())
    auto_send = db.Column(db.Boolean())
    frequency = db.Column(db.String())
    day_of_week = db.Column(db.String())


    def __init__(self, message_type, message, auto_send=False, frequency='weekly', day_of_week='saturday'):
        self.message_type = message_type
        self.message = message
        self.auto_send = auto_send
        self.frequency = frequency
        self.day_of_week = day_of_week

    def __repr__(self):
        return f'{self.message}'








































