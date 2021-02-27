from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# from sms import send_message

from config import redis_client
# from database import Members, Messages



app = Flask(__name__)
app.config.from_object(str(redis_client.get('APP_SETTINGS').decode('utf-8')))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# from database import Members, Messages

class Members(db.Model):
    tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    # is_subscriber = db.Column(db.Boolean())

    def __init__(self, first_name, last_name):
        #    self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f'{self.last_name}, {self.first_name}'


@app.route('/user-add', methods=['GET', 'POST'])
def user_add():
    request_data = request.get_json()
    name = request_data['name']
    new_user = Members(str(name), 'Deubner')
    db.session.add(new_user)
    db.session.commit()

    evan = Members.query.filter_by(first_name='Evan').first()
    my_name = evan.first_name

    return (f'The name is {my_name}')

@app.route('/')
def index():
    return jsonify(users)
# te('/message/send', methods={'GET', 'POST'})
#def send():
#    # send_message(number, user_number, user_message)
#    message_type = str(request.args['type'])
#    message = Messages(type=message_type)
#    message_ready = message.get()[2]
#
#    for user in db.lrange("USER", 0, db.llen("USERS")):
#        current_user = User(name=str(user.decode('utf-8')))
#        try:
#            user_number = int(current_user.get()[1])
#        except ValueError:
#            user_number = 18162882093
#        responseData = sms.send_message(
#                {
#                    "fmerom": number,
#                    "to": user_number,
#                    "text": message_ready,
#                }
#            )
#        if responseData["messages"][0]["status"] == "0":
#            print("Message sent!")
#        else:
#            print(f"Message failed -> {responseData['messages'][0]['error-text']}")
#

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False)


