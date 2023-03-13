import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    # Connect User to WebSocket
    async def connect(self):
        # Declare Room Name
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Connect to Redis server
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    # Disconnect from WebSocket
    async def disconnect(self, close_code):
        # Disconnect from Redis Server
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive data from user
    async def receive(self, text_data): 
        username = self.scope["user"].username
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        message = (message)

        # Send a message to the chatroom based on the room name
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'sender':username,
                'message':message,
            }
        )
    # Send a new message
    async def chat_message(self, event):
        message = event['message']
        username = self.scope["user"].username

        await self.send(text_data=json.dumps({
            'message':message,
            'username':username,
            'sender':event['sender']
        }))
