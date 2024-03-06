from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from .models import Category,Auction,Bid,Product,UserSearch,UserBid
from .forms import CategoryForm,BidForm,AuctionForm
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from .decorators import seller_required
from .recommendations import auction_recommendation

#CRUD operation for category starts
@login_required
@seller_required
def category_list(request):
    category_list = Category.objects.all()
    context = {'category_list':category_list}
    return render(request,'main_app/category/category_list.html',context)

@login_required
@seller_required
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

@login_required
@seller_required  
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

@login_required
@seller_required
def category_delete(request,pk):
    data = get_object_or_404(Category,id=pk)
    data.is_active=False
    data.save()
    return redirect('category-list')
#Ends category crud

#Auction Crud starts here

@login_required
@seller_required
def auction_list(request):
    auctions = Auction.objects.filter(seller=request.user)
    
    context = {
        'auctions':auctions
    }
    return render(request,'main_app/Auction/auction_list.html',context)


@login_required
@seller_required
def auction_create(request):
    if request.method == 'POST':
        form = AuctionForm(request.POST,request.FILES)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.seller = request.user
            auction.save()
            return redirect('auction-list')
    else:
        form = AuctionForm()

    context = {'form': form}
    return render(request, 'main_app/Auction/auction_create.html', context)
    
@login_required
@seller_required
def auction_update(request, pk):
    data = get_object_or_404(Auction, id=pk)

    if request.method == 'POST':
        form = AuctionForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            # Handle file field update
            if 'image' in form.changed_data:
                # Clear the existing file
                if data.image:
                    default_storage.delete(data.image.path)
                # Save the new file
                image_file = form.cleaned_data['image']
                data.image.save(image_file.name, ContentFile(image_file.read()))

            form.save()
            return redirect('auction-list')
    else:
        form = AuctionForm(instance=data)

    context = {'form': form, 'auction': data}

    return render(request, 'main_app/Auction/auction_update.html', context)


#Home page view of the website
@login_required
def home(request):
    if request.user.role == 'Buyer':
        auctions = Auction.objects.filter(auction_status='open')
    else:
        auctions = Auction.objects.all()

    recommended_auctions = auction_recommendation(request)
    # if recommended_auctions:
    #     auctions = list(auctions) + list(recommended_auctions.values())
    
    context = {
        'recommended_auctions':recommended_auctions,
        'auctions':auctions
    }
    return render(request,'main_app/Auction/home.html',context)

def homeSearch(request):
    query = request.GET.get('q')
    #storing the query searched by user for using it to recommend items
    UserSearch.objects.create(user=request.user, searchQuery=query)
    if request.user.role == 'Buyer':
        auctions = Auction.objects.filter(title__icontains=query,auction_status='open')
    else:
        auctions = Auction.objects.filter(title__icontains=query)
    
    context = {
        'auctions':auctions
    }
    return render(request,'main_app/Auction/home.html',context)

@login_required
def home_particular_category(request,pk):
    category = get_object_or_404(Category,id=pk)
    if request.user.role == 'Buyer':
        auctions = Auction.objects.filter(auction_status='open',category=category)
    else:
        auctions = Auction.objects.filter(category=category)
    
    context = {
        'category':category,
        'auctions':auctions
    }
    return render(request,'main_app/Auction/home.html',context)


@login_required
@seller_required
def update_auction_status(request, pk):
    data = get_object_or_404(Auction, id=pk)
    print(data.auction_status)

    if request.method == 'POST':
        data.auction_status == 'closed'
        data.save()
        return JsonResponse({'status':'success','auction_status':data.auction_status})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)

@login_required
def auction_detail(request, pk):
    auction = get_object_or_404(Auction, id=pk)
    form = BidForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            bid_value = form.cleaned_data['bid_value']
            #storing data to use for recommendations
            UserBid.objects.create(user=request.user, auction=auction, bid_value=bid_value, category=auction.category)
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
                auction_details = {
                'bid_value': auction.get_max_bid(),
                # Add other details as needed
            }

            return JsonResponse(auction_details)

    context = {
        'auction': auction,
        'form': form,
    }

    return render(request, 'main_app/Auction/auction_detail.html', context)
