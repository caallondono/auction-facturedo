from django.contrib.auth.models import User
from rest_framework import serializers

from apps.auction.models import Auction, Bid


class AuctionSerializer(serializers.HyperlinkedModelSerializer):
    """"""

    def validate(self, attrs):

        # Validates if an auction is created with 'closed' status only por PUT method
        if (
                self.context.get('request') and
                self.context.get('request', {}).method != "PUT" and
                attrs.get('status') == Auction.OPT_STATUS_CLOSED
        ):
            raise serializers.ValidationError("An auction must be created with 'open' status")
        return attrs

    class Meta:
        model = Auction
        fields = ('id', 'amount', 'status')


class BidSerializer(serializers.HyperlinkedModelSerializer):
    """"""

    user = serializers.PrimaryKeyRelatedField(read_only=True, source='user.username')

    def validate(self, attrs):

        # Validates if an user has an active bind for a specific auction
        result = Bid.objects.filter(user=attrs.get('user'), auction=attrs.get('auction'), winner=False)
        if len(result) > 0 and not attrs.get('id'):
            raise serializers.ValidationError(
                f"The user '{attrs.get('user', {}).username}' has an active bid for this auction")
        return attrs

    class Meta:
        model = Bid
        fields = ('id', 'user', 'amount', 'discount_rate', 'winner')
