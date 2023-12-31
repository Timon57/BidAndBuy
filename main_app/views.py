from django.shortcuts import render,get_object_or_404,redirect
from .models import Category,Auction,Bid,Product
from .forms import CategoryForm,BidForm
from django.contrib import messages

#CRUD operation for category stars
def category_list(request):
    category_list = Category.objects.all()
    context = {'category_list':category_list}
    return render(request,'main_app/category/category_list.html',context)

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm()
        context = {'form':form}
        return render(request,'main_app/category/category_create.html',context)
    
def category_update(request,pk):
    data = get_object_or_404(Category,id=pk)
    form = CategoryForm(instance=data)
    context = {'form':form}
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    return render(request,'main_app/category/category_update.html',context)

def category_delete(request,pk):
    data = get_object_or_404(Category,id=pk)
    data.is_active=False
    data.save()
    return redirect('category-list')
#Ends category crud

#Home page view of the website
def home(request):
    products = Product.objects.all()
    context = {
        'products':products
    }
    return render(request,'home.html',context)



#Auction 
def auction_home(request):
    auctions = Auction.objects.filter(auction_status='open')
    
    context = {
        'auctions':auctions
    }
    return render(request,'main_app/Auction/auction_home.html',context)

def auction_detail(request, pk):
    auction = get_object_or_404(Auction, id=pk)
    form = BidForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            bid_value = form.cleaned_data['bid_value']

            # Perform your custom validation here
            if bid_value <= auction.starting_price:
                messages.error(request, 'Bid value must be greater than the starting price.')
            if bid_value <= auction.get_max_bid():
                messages.error(request, 'Bid value must be greater than the current higest price.')
            else:
                bid = form.save(commit=False)
                bid.bidder = request.user
                bid.auction_id = auction
                bid.save()
                return redirect('auction-detail', pk=pk)

    context = {
        'auction': auction,
        'form': form,
    }

    return render(request, 'main_app/Auction/auction_detail.html', context)

        

