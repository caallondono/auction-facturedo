from django.urls import path

from apps.auction import views

urlpatterns =[
    path('', views.get_all_auctions)
]