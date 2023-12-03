from django.urls import path
from .import views
urlpatterns = [
    path('',views.home,name='home'),
    path('auction/',views.auction_home,name='auction-home'),
    path('categories/',views.category_list,name="category-list"),
    path('category/create',views.category_create,name='category-create'),
    path('category/update/<str:pk>',views.category_update,name='category-update'),
    path('cateogry/delete/<str:pk>',views.category_delete,name='category-delete'),
    
]
