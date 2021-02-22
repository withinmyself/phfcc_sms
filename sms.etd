

from data.users import Users, Messages
import config
from config import *







user = Users("Evan", 18162882093)
message = Messages("Covid", "Covid tests available")
redis_client.set(user.name, user.get())
redis_client.set(message.type, message.get())


def send_message(number, user_number, user_message):

    responseData = sms.send_message(
        {
            "from": number,
            "to": user_number,
            "text": user_message,
        }
    )
    if responseData["messages"][0]["status"] == "0":
        print("Message sent!")
    else:
        print(f"Message failed -> {responseData['messages'][0]['error-text']}")

