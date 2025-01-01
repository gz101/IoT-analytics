import json

from channels.generic.websocket import AsyncWebsocketConsumer


class IoTConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.device_name = self.scope["url_route"]["kwargs"]["device_name"]
        self.group_name = f"device_{self.device_name}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "iot.message",
                "data": data
            }
        )

    async def iot_message(self, event):
        await self.send(text_data=json.dumps(event["data"]))
