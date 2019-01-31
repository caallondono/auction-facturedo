from django.contrib import admin
from apps.auction.models import Auction
from apps.auction.models import Bid


admin.site.register(Auction)
admin.site.register(Bid)


class AuctionAdmin(admin.ModelAdmin):
    fields = ('id', 'amount', 'status')


class BidAdmin(admin.ModelAdmin):
    fields = ('id', 'auction', 'user', 'amount', 'discount_rate', 'winner')
