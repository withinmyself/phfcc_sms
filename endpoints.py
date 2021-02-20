from flask import Flask, jsonify, request
from sms import send_message
from data.database import Messages, User, db
import redis
from config import *


app = Flask(__name__)

@app.route('/message/get', methods={'GET', 'POST'})
def get_message():
    message_type = str(request.args['type'])
    messages = Messages(type=message_type)
    return messages.get()[2]

@app.route('/message/set', methods={'GET', 'POST'})
def set_message():
    message_type = str(request.args['type'])
    new_message = str(request.args['message'])
    try:
        messages = Messages(type=message_type)
    except redis.exceptions.ResponseError as error:
        print(f"Received error -> {error} : Might be missing quotes around keyword?")
        return f"{error}"
    messages.change_message(new_message=new_message)
    return messages.get()[2]
    

@app.route('/message/send', methods={'GET', 'POST'})
def send():
    # send_message(number, user_number, user_message)
    message_type = str(request.args['type'])
    message = Messages(type=message_type)
    message_ready = message.get()[2]

    for user in db.lrange("USER", 0, db.llen("USERS")):
        current_user = User(name=str(user.decode('utf-8')))
        try:
            user_number = int(current_user.get()[1])
        except ValueError:
            user_number = 18162882093
        responseData = sms.send_message(
                {
                    "from": number,
                    "to": user_number,
                    "text": message_ready,
                }
            )
        if responseData["messages"][0]["status"] == "0":
            print("Message sent!")
        else:
            print(f"Message failed -> {responseData['messages'][0]['error-text']}")

@app.route('/put', methods={'GET', 'POST'})
def put():
    name = str(request.args['name'])
    id = str(request.args['id'])
    list = (name, id)
    return id

if __name__ == '__main__':
    app.run()

