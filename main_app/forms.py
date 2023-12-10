from .models import Category,Bid as Bid
from django.forms import ModelForm

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        exclude = ['is_active']

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["bid_value"]