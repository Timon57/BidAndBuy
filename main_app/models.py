from django.db import models
from django.urls import reverse
from bidandbuy.settings import AUTH_USER_MODEL
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
from django.db.models import Max
from django.utils import timezone

class Category(models.Model):

    IS_ACTIVE_CHOICES = (
    (True, 'Active'),
    (False, 'Inactive'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(choices=IS_ACTIVE_CHOICES,default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    discount = models.IntegerField(
        validators = [MinValueValidator(0),MaxValueValidator(99)]
    )
    actual_price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    
    def save(self, *args, **kwargs):
        price_decimal = Decimal(str(self.price))
        self.actual_price = price_decimal - (Decimal(str(self.discount)) / 100)*price_decimal
        super(Product,self).save(*args,**kwargs)

    def __str__(self):
        return self.title

class Auction(models.Model):

    def clean(self):
        """
        Custom validation to ensure start_datetime is before end_datetime.
        """
        if self.start_datetime and self.end_datetime and self.start_datetime >= self.end_datetime:
            raise ValidationError("Start datetime must be before end datetime.")
        
    AUCTION_STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('open', 'open'),
        ('closed', 'Closed'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    auction_status = models.CharField(max_length=20, choices=AUCTION_STATUS_CHOICES, default='draft')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    seller = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='auctions')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
   
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Auctions'

    def get_absolute_url(self):
        return reverse("auction-detail", args=[self.pk])
    
    def get_max_bid(self):
        return Bid.get_max_bid_for_auction(self.id)
    
    def get_remaining_time(self):
        now = timezone.now()

        if now < self.start_datetime:
            return "Auction has not started yet."
        elif now > self.end_datetime:
            return "Auction has ended."

        remaining_time = self.end_datetime - now
        return remaining_time
    
    

class Bid(models.Model):
    bidder = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bid_owner")
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bid_listing")
    bid_value = models.DecimalField(max_digits=10, decimal_places=2)
    bid_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.bid_value)

    

        
    @staticmethod
    def get_max_bid_for_auction(auction_id):
        max_bid = Bid.objects.filter(auction_id=auction_id).aggregate(Max('bid_value'))['bid_value__max']
        return max_bid or 0
    


