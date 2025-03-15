import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone

from .models import Message


class ChatConsumer(WebsocketConsumer):
    """ Chat Consumer for handling WebSocket connections """
    def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f'chat_{self.id}'
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        # Accept connection
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    
    def receive(self, text_data):
        """ Receive message from WebSocket """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat(),
            }
        )

    """ Receive message from room group """
    def chat_message(self, event):
        # Send message to websocket
        self.send(text_data=json.dumps(event))
