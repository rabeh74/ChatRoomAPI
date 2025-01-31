from channels.generic.websocket import AsyncWebsocketConsumer
import json

from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user = self.scope['url_route']['kwargs']['username']
        self.room_group_name = f'chat_{self.room_name}'
        

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Send message to room group that user has joined the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'welcome_message',
                'message': f'{self.user} has joined the room'
            }
        )
        
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user = text_data_json['user']
        message = text_data_json['message']
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        message = f"{user}: {message}"
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user
        }))
    async def welcome_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message,
        }))