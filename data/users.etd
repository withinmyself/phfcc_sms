

class Users():
    """
    Used to save user information in Redis
    """
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def get(self):
        return self.number

class Messages():
    """
    Used to save messages in Redis
    """
    def __init__(self, type, message, auto=False):
        self.type = type
        self.message = message
        self.auto = auto

    def get(self):
        return self.message

    def is_auto(self):
        if auto:
            return True
        else:
            return False