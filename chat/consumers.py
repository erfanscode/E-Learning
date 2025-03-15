import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone

from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    """ Chat Consumer for handling WebSocket connections """
    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f'chat_{self.id}'
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # Accept connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def persist_message(self, message):
        """ Persist message to database """
        await Message.objects.acreate(
            user=self.user,
            course_id=self.id,
            content=message
        )
    
    async def receive(self, text_data):
        """ Receive message from WebSocket """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat(),
            }
        )
        # Persist message
        await self.persist_message(message)

    """ Receive message from room group """
    async def chat_message(self, event):
        # Send message to websocket
        await self.send(text_data=json.dumps(event))
