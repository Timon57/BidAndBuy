from .models import Category,Bid,Auction
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils import timezone

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        exclude = ['is_active']

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["bid_value"]

class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        exclude = ['seller','auction_status']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control mb-1'})


