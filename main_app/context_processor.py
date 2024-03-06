from .models import Category,Auction
def categories(request):
    user_id = request.user.id  # Assuming `request` is available
    win_auction = get_winning_auctions_for_user(user_id)

    return{
        'categories':Category.objects.all(),
        'win_auction':win_auction
    }

def get_winning_auctions_for_user(user_id):
    winning_auctions = Auction.objects.filter(winner=user_id)
    return winning_auctions