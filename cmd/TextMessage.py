class TextMessage:
    def __init__(self, phone=None, recipient=None, message=None, received=None):
        self.phone = phone
        self.recipient = recipient
        self.message = message
        self.received = received

    def to_string(self):
        return f"From: {self.phone} Received on: {self.received} Message: {self.message}"
