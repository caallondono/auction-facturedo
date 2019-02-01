from django.contrib import admin
from apps.auction.models import Auction
from apps.auction.models import Bid


class AuctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'status')


class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'auction', 'user', 'amount', 'discount_rate', 'winner')


admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
