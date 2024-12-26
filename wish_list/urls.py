from django.urls import path
from . import views

urlpatterns = [
    path('', views.wish_list_summary, name='wish_list_summary'),
    path('add/', views.wish_list_add, name='wish_list_add'),
    path('delete/', views.wishlist_delete, name='wishlist_delete'),

]