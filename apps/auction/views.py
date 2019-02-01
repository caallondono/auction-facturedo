from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.auction.models import Auction, Bid
from apps.auction.serializers import AuctionSerializer, BidSerializer


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny, ))
def auction_list_create(request):
    """End-point for listing and creating auctions"""

    if request.method == 'GET':
        """Lists all auctions"""

        auctions = Auction.objects.all()
        serializer = AuctionSerializer(auctions, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        """Creates new auction after validations"""

        # Returns error when id field is specified in request data. Id must be used only for update proposes
        if request.data.get('id'):
            data_response = {'non_field_errors': ['Use PUT method for updating']}
            return Response(data_response, status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('status') == Auction.OPT_STATUS_CLOSED:
            data_response = {'non_field_errors': ['New auctions cannot be closed']}
            return Response(data_response, status=status.HTTP_400_BAD_REQUEST)

        serializer = AuctionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes((permissions.AllowAny, ))
def auction_status_update(request, pk):
    """End-point fro updating auctions"""

    if request.method == 'PUT':
        """Updates status field of an auction"""

        try:
            auction = Auction.objects.get(pk=pk)
        except Auction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = {"status": request.data.get('status', '')}
        context = {'request': request}
        serializer = AuctionSerializer(auction, data=data, partial=True, context=context)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny, ))
def bid_list_and_create(request):
    """End-point for listing and creating auctions"""

    if request.method == 'GET':
        """Lists all bids"""

        bids = Bid.objects.all()
        context = {'request': request}
        serializer = BidSerializer(bids, many=True, context=context)
        return Response(serializer.data)

    if request.method == 'POST':
        """Creates new bid after validations"""

        # Returns error when id field is specified in request data. Id must be used only for update proposes
        if request.data.get('id'):
            data_response = {'non_field_errors': ['Use PUT method for updating']}
            return Response(data_response, status=status.HTTP_400_BAD_REQUEST)

        # TODO: Calculate all bids amounts of the auction
        # TODO: If the auction is achieved, select bid winners and close the auction

        serializer = BidSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
