from django.contrib.auth.models import User
from rest_framework import serializers

from apps.auction.models import Auction, Bid


class AuctionSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Auction model"""

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
    """Serializer for Bid model"""

    username = serializers.ReadOnlyField(source='user.username')
    user = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all(), required=True)
    auction = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Auction.objects.all(), required=True)

    def validate(self, attrs):

        # Validates if an user has an active bind for a specific auction
        result = Bid.objects.filter(user=attrs.get('user'), auction=attrs.get('auction'), winner=False)
        if len(result) > 0 and not attrs.get('id'):
            raise serializers.ValidationError(
                f"The user '{attrs.get('user', {}).username}' has an active bid for this auction")

        # TODO: Winner field must be generated automatically

        return attrs

    class Meta:
        model = Bid
        fields = ('id', 'user', 'username', 'amount', 'auction', 'discount_rate', 'winner')
