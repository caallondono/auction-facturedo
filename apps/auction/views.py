from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.auction.models import Auction
from apps.auction.serializers import AuctionSerializer


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def get_all_auctions(request):

    if request.method == 'GET':
        auctions = Auction.objects.all()
        serializer = AuctionSerializer(auctions, many=True)
        return Response(serializer.data)
