from django.db.models import Sum
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

        # If sum of auction bids is not complete, avoid closing state
        total_amount = Bid.objects.filter(auction_id=pk).aggregate(Sum('amount'))
        if not total_amount.get('amount__sum'):
            total_amount['amount__sum'] = 0

        if request.data.get('status') == Auction.OPT_STATUS_CLOSED and total_amount.get('amount__sum') < auction.amount:
            data_response = {'non_field_errors': ['This auction cannot be closed. Total amount is not achieved']}
            return Response(data_response, status=status.HTTP_400_BAD_REQUEST)

        data = {"status": request.data.get('status', '')}
        context = {'request': request}
        serializer = AuctionSerializer(auction, data=data, partial=True, context=context)

        if serializer.is_valid():
            serializer.save()

            if request.data.get('status') == Auction.OPT_STATUS_CLOSED:
                # Selects bids winners
                selected_bids = Bid.objects.filter(auction_id=pk).order_by('discount_rate')

                total_bids = 0
                for selected_bid in selected_bids:
                    selected_bid.winner = True
                    selected_bid.save()
                    total_bids += selected_bid.amount

                    if total_bids >= auction.amount:
                        break

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

        # Validates if bid auction is close
        bid_auction = Auction.objects.get(id=request.data.get("auction"))
        if bid_auction.status == Auction.OPT_STATUS_CLOSED:
            data_response = {'non_field_errors': ['This auction is close']}
            return Response(data_response, status=status.HTTP_400_BAD_REQUEST)

        serializer = BidSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
