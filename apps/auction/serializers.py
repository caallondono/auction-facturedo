from rest_framework import serializers

from apps.auction.models import Auction, Bid


class AuctionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Auction
        fields = ('amount', 'status')


class BidSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bid
        fields = ('amount', 'discount_rate', 'winner')
