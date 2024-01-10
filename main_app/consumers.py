import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Bid
from asgiref.sync import async_to_sync

class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.auction_id = self.scope['url_route']['kwargs']['auction_id']
        self.auction_group_name = f"auction_{self.auction_id}"

        await self.channel_layer.group_add(
            self.auction_group_name,
            self.channel_name
        )

        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected!'
        }))

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.auction_group_name,
            self.channel_name
        )

        await self.send(text_data=json.dumps({
            'type': 'connection_closed',
            'message': 'Connection closed by the server.'
        }))

    async def receive(self, text_data):
        bid_data = json.loads(text_data)
        bid_value = bid_data['bid_value']

        # Save the bid
        bid = Bid.objects.create(
            bidder=self.scope['user'],
            auction_id=self.auction_id,
            bid_value=bid_value
        )

        # Send bid update to auction group
        await self.channel_layer.group_send(
            self.auction_group_name,
            {
                'type': 'bid_update',
                'bid_value': bid_value
            }
        )

    # Receive bid update from auction group
    async def bid_update(self, event):
        bid_value = event['bid_value']

        # Send bid update to WebSocket
        await self.send(text_data=json.dumps({
            'bid_value': bid_value
        }))