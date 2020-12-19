import asyncio
from channels.consumer import SyncConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class EchoConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print(self.scope)
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        print(f'EVENT {event}')
        self.send({
            "type": "websocket.send",
            "text": event["text"],
        })


class TickTockConsumer(AsyncJsonWebsocketConsumer):

    async  def connect(self):
        await self.accept()
        while 1:
            await  asyncio.sleep(1)
            await self.send_json("tick")
            await  asyncio.sleep(1)
            await self.send_json(".......tock")


class StatusConsumer(AsyncJsonWebsocketConsumer):
    room_group_name = 'notify'

    async def connect(self):
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name, 
            self.channel_layer
        )

    async def analytic_progress(self, event):
        await self.send_json(event)