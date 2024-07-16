import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User

from asgiref.sync import sync_to_async


class Calculator(AsyncWebsocketConsumer):
    async def connect(self, userid=None):
        self.room_group_name = "counter"
        # userid = self.scope["url_route"]["kwargs"]["userid"]
        # res = await sync_to_async(User.objects.get)(id=userid)
        # if res.is_superuser:
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

   

    # Receive message from room group
    async def send_notification(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
