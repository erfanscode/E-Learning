import json

from channels.generic.websocket import WebsocketConsumer

from .models import Message


class ChatConsumer(WebsocketConsumer):
    """ Chat Consumer for handling WebSocket connections """
    def connect(self):
        # Accept connection
        self.accept()

    def disconnect(self, close_code):
        # Close connection
        pass
    
    def receive(self, text_data):
        """ Receive message from WebSocket """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to websocket
        self.send(
            text_data=json.dumps({
                'message': message
            })
        )
