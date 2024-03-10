from django.core import serializers
from django.http import JsonResponse
import pandas as pd
import json
from.models import Auction,UserSearch,UserBid,Category
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from operator import itemgetter


#get the user's interactions data stored
def get_user_interactions(user):

    user_searches = list(UserSearch.objects.filter(user=user).values_list('searchQuery',flat=True))
    user_bids = list(UserBid.objects.filter(user=user).values_list('category__name', flat=True))
    return user_searches,user_bids


#get all the auction data in json format
def auction_data(request):
    auctions = Auction.objects.filter(auction_status='open')
    data = serializers.serialize('json',auctions)
    return JsonResponse(json.loads(data),safe=False)

def process_auction_data(json_data):
    auctions = json.loads(json_data)
    
    # Fetch category names based on category IDs
    category_ids = [auction['fields']['category'] for auction in auctions]
    category_names = {category.id: category.name for category in Category.objects.filter(id__in=category_ids)}
    
    # Extract relevant fields from each auction
    auction_data = {
        'id': [auction['pk'] for auction in auctions],  # Extract 'id' field
        'description': [auction['fields']['description'] for auction in auctions],
        'starting_price': [auction['fields']['starting_price'] for auction in auctions],
        'category': [category_names.get(auction['fields']['category'], '') for auction in auctions]
    }
    
    return auction_data


def auction_recommendation(request):
    #Get user's interaction data
    user_searches, user_bids = get_user_interactions(request.user)
    
    # Combine user searches and bids into a single list and make dataFrame
    if user_searches and user_bids:
        user_data = ' '.join(user_searches + user_bids)
    elif user_searches:
        user_data = ' '.join(user_searches)
    elif user_bids:
        user_data = ' '.join(user_bids)
    else:
        user_data = []
    user_df = pd.Series(user_data)
    # print('---user data--')
    # print(user_df)
    


    #Calculate similarity scores between user's interactions and item descriptions
    if user_data :
        
        # Process auction data
        json_data = auction_data(request).content
        data = process_auction_data(json_data)
        df = pd.DataFrame(data)
        # print('---data---')
        # print(df)
        df['description'] = df['description'].fillna("")
        df['overview'] = df['category'].fillna("")
        df['text_data'] = df['description'] + ' ' + df['category']
        # print(df['text_data'])

        #Vectorize the text data
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(df['text_data'])
        # print('----auction item vector---')
        # print(tfidf_matrix)

        #Vectorize the users data
        tfidf_user_matrix = tfidf.transform(user_df)
        # print('---user data vector----')
        # print(tfidf_user_matrix)


        #calclucate cosine similarity
        cosine_sim = cosine_similarity(tfidf_matrix,tfidf_user_matrix)
        # print('--cosine similarity matrix--')
        # print(cosine_sim)

         # Get indices of top five highest similarity scores
        top_indices = cosine_sim.argsort(axis=0)
        print(top_indices)
        length = len(top_indices)

        top_indices = cosine_sim.argsort(axis=0)[-3:]
        print(top_indices)


        # Get IDs of most similar items
        top_item_ids = df.iloc[top_indices.flatten()]['id'].tolist()
        # print(top_item_ids)

        # Retrieve Auction objects for the most similar items
        top_auctions = Auction.objects.filter(id__in=top_item_ids)
        # print(top_auctions)

        return top_auctions
    
        
        
        
    
       
        


        
