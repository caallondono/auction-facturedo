from django.urls import path

from apps.auction import views

urlpatterns =[
    path('', views.auction_list_create),
    path('change-status/<int:pk>', views.auction_status_update),
    path('bid/', views.bid_list_and_create),
]
