import redis

db = redis.Redis()

class User():
    def __init__(self, name, phone_number="not set", subscriber="True"):
        self.name = name 
        self.phone_number = phone_number
        self.subscriber = subscriber
        
        self._set()

    def _set(self):

        db.lpush(self.name, self.name)
        db.lpush(self.name, self.phone_number)
        db.lpush(self.name, self.subscriber)
        db.lpush("USER", self.name)

    def add(self):
        db.lset(self.name, 0, "True")
        return "Successfully subscribed to service"

    def remove(self):
        db.lset(self.name, 0, "False")
        return "You have been removed from our service"

    def edit(self, name=None, phone_number=None):
        x = 0
        y = 0
        if name != None:
            db.lset(self.name, 2, name)
            x = 1
        if phone_number != None:
            db.lset(self.name, 1, phone_number)
            y = 1
        if x == 0 and y == 1:
            return "Your name has been changed"
        elif x == 1 and y == 0:
            return "Your phone number has been changed"
        elif x == 1 and y == 1:
            return "Your name and phone number have both been changed"
        elif x == 0 and y == 0:
            return "Nothing has been changed"


    def get(self):
        user_info = []
        for item in db.lrange(self.name, 0, 2):
            user_info.append(item.decode('utf-8'))
        return user_info



class Messages():
    def __init__(self, type="not set", message="not set", schedule="weekly", running="True"):
        self.type = type 
        self.message = message 
        self.schedule = schedule 
        self.running = running 

        self._set()

    def _set(self):
        if db.lindex(self.type, 3) != b'self.type':

            db.lpush(self.type, self.type)
            db.lpush(self.type, self.message)
            db.lpush(self.type, self.schedule)
            db.lpush(self.type, self.running)

    def start(self):
        db.lset(self.type, 0, "True")
        return "Successfully started"

    def stop(self):
        db.lset(self.type, 0, "False")
        return "Successfully stopped"

    def time(self, time):
        options = ["monthly", "weekly", "daily"]
        if time not in options:
            return "You have entered a time that is currently not supported"
        else:
            db.lset(self.type, 1, time)
            return "Success"

    def change_message(self, new_message):
        db.lset(self.type, 2, new_message)
        return "Message has been changed"

    def get(self):
        message = []
        for item in db.lrange(self.type, 0, 3):
            message.append(item.decode('utf-8'))
        return message


user = User("ET", 18162882093)