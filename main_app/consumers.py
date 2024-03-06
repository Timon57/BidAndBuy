import json
from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
from .models import Bid,Auction
from django.shortcuts import get_object_or_404
from channels.db import database_sync_to_async
from django.utils import timezone
from django.db.models import Max


class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.auction_id = self.scope['url_route']['kwargs']['auction_id']
        self.auction_group_name = f"auction_{self.auction_id}"
        await self.channel_layer.group_add(
            self.auction_group_name,
            self.channel_name
        )
        await self.accept()
        
        remaining_time =  await self.get_remaining_time(self.auction_id)
        await self.send(text_data=json.dumps({
            'type': 'time_update',
            'remaining_time': remaining_time
            
        }))


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.auction_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        bid_data = json.loads(text_data)
        bid_value = bid_data['bidValue']

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
        highest_bidder = await self.get_highest_bidder_name(self.auction_id)
        remaining_time =  await self.get_remaining_time(self.auction_id)
        await self.send(text_data=json.dumps({
            'type': 'bid_update',
            'bid_value': bid_value,
            'highest_bidder': highest_bidder,
            'remaining_time': remaining_time
            
        }))
    @database_sync_to_async
    def get_highest_bidder_name(self, auction):
        max_bid = Bid.objects.filter(auction_id=auction).order_by('-bid_value').first()
        highest_bidder = max_bid.bidder.username if max_bid else None
        return highest_bidder
    
    @database_sync_to_async
    def get_remaining_time(self,auction_id):
        auction = Auction.objects.get(id = auction_id)
        now = timezone.now()

        if now < auction.start_datetime:
            return "Auction has not started yet."
        elif now > auction.end_datetime:
            return "Auction has ended."

        remaining_time = auction.end_datetime - now
        return remaining_time.total_seconds()
    


class AuctionHomeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        auctions_ids = await self.get_all_auction_ids()

        for auction_id in auctions_ids:
            await self.subscribe_to_auction(auction_id)
            


    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass


    async def subscribe_to_auction(self,auction_id):
        auction_group_name = f"auction_{auction_id}"
        await self.channel_layer.group_add(
            auction_group_name,
            self.channel_name
        )
        remaining_time =  await self.get_remaining_time(auction_id)
        # maximum_bid = await self.get_max_bid_for_auction(auction_id)
        await self.send(text_data=json.dumps({
            'type': 'time_update',
            'auction_id':auction_id,
            # 'maximum_bidd' : maximum_bid,
            'remaining_time': remaining_time
            
        }))

    @database_sync_to_async
    def get_remaining_time(self,auction_id):
        auction = Auction.objects.get(id = auction_id)
        now = timezone.now()

        if now < auction.start_datetime:
            return "Auction has not started yet."
        elif now > auction.end_datetime:
            return "Auction has ended."

        remaining_time = auction.end_datetime - now
        return remaining_time.total_seconds()


    @database_sync_to_async
    def get_all_auction_ids(self):
        return list(Auction.objects.filter(auction_status='open').values_list('id', flat=True))
    
    @database_sync_to_async
    def get_highest_bidder_name(self, auction_id):
        max_bid = Bid.objects.filter(auction_id=auction_id).order_by('-bid_value').first()
        highest_bidder = max_bid.bidder.username if max_bid else None
        return highest_bidder
    
    @database_sync_to_async
    def get_max_bid_for_auction(self,auction_id):
        max_bid = Bid.objects.filter(auction_id=auction_id).aggregate(Max('bid_value'))['bid_value__max']
        return float(max_bid) or 0
    
    



