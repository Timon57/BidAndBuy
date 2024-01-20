from django.urls import path
from .import views
urlpatterns = [
    path('',views.home,name='home'),
    path('auction/',views.auction_list,name='auction-list'),
    path('auction/create/',views.auction_create,name='auction-create'),
    path('auction/<str:pk>',views.auction_detail,name='auction-detail'),
    path('auction/update/<str:pk>',views.auction_update,name='auction-update'),
    path('auction/update/status/<str:pk>',views.update_auction_status,name='auction-update-status'),
    path('categories/',views.category_list,name="category-list"),
    path('category/create',views.category_create,name='category-create'),
    path('category/update/<str:pk>',views.category_update,name='category-update'),
    path('cateogry/delete/<str:pk>',views.category_delete,name='category-delete')
    
]
