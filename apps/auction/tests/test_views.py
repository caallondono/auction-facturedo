from django.contrib.auth.models import User
from django.test import TestCase
from mock import patch, MagicMock
from rest_framework import status
from rest_framework.test import APIClient

from apps.auction.models import Auction, Bid


class FakeBid:

    winner = False
    amount = 0.0

    def __init__(self, winner, amount):
        self.winner = winner
        self.amount = amount

    def __str__(self):
        return f"W: {self.winner} - A: {self.amount}"

    def save(self):
        pass


class AuctionListCreateTest(TestCase):
    """Unit tests for listing and creating auctions using endpoints"""

    endpoint = "/auction/"

    def setUp(self):
        # User for testing
        self.user = User(username="user_test1")
        self.user.save()

        # Create auctions and bids for testing proposes
        self.auction1 = Auction(amount=100)
        self.auction2 = Auction(amount=200)
        self.auction1.save()
        self.auction2.save()

        self.client = APIClient()

    def test_methods_not_allowed(self):
        """Verify error response when client uses methods not allowed"""
        response = self.client.put(self.endpoint, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_getting_all_auctions(self):
        """Verify response when client requests for auctions"""
        response = self.client.get(self.endpoint, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_check_creation_error_when_id(self):
        """Verify error when client tries to create auction with id"""
        data = {"id": 1}
        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], 'Use PUT method for updating')

    def test_check_creation_error_when_status_closed(self):
        """Verify error when client tries to create auction with status closed"""
        data = {"status": Auction.OPT_STATUS_CLOSED}
        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], 'New auctions cannot be closed')

    def test_when_creation_serializer_validation_is_not_correct(self):
        """Verify error when serializer validation raise an error during creation"""
        data = {}
        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_when_creation_request_is_correct(self):
        """Verify correct creation"""
        data = {"amount": 200}
        response = self.client.post(self.endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AuctionChangeStatusTest(TestCase):
    """Unit tests for changing the auction status using endpoints"""

    endpoint = "/auction/change-status/"

    def setUp(self):
        # User for testing
        self.user = User(username="user_test1")
        self.user.save()

        # Create auctions and bids for testing proposes
        self.auction1 = Auction(amount=100)
        self.auction2 = Auction(amount=200)
        self.auction1.save()
        self.auction2.save()
        bids_data = [
            Bid(user=self.user, auction=self.auction1, amount=40, discount_rate=1.0),
            Bid(user=self.user, auction=self.auction2, amount=30, discount_rate=1.1)
        ]
        self.bids = Bid.objects.bulk_create(bids_data)

        self.client = APIClient()

    def test_methods_not_allowed(self):
        """Verify error response when client uses methods not allowed"""
        response = self.client.post(f"{self.endpoint}1", {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_when_auction_does_not_exists(self):
        """Verify error when auction does not exists"""
        response = self.client.put(f"{self.endpoint}0", {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('apps.auction.models.Bid.objects.filter')
    def test_when_total_amount_is_not_calculated_or_lower(self, mock_bid_filter):
        """Verify response when total amount is set to 0 or lower than auction amount when is not calculated in query"""

        mock_aggregate = MagicMock()
        mock_aggregate.aggregate.return_value = {"amount__sum": 20}
        mock_bid_filter.return_value = mock_aggregate

        data = {"status": "closed"}
        response = self.client.put(f"{self.endpoint}{self.auction1.id}", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get('non_field_errors')[0],
            'This auction cannot be closed. Total amount is not achieved'
        )

    def test_when_serializer_validation_is_not_correct(self):
        """Verify error when serializer validation raise an error during creation"""
        data = {"status": "abcd"}
        response = self.client.put(f"{self.endpoint}{self.auction1.id}", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('apps.auction.models.Bid.objects.filter')
    def test_when_serializer_validation_is_correct_and_there_are_winners_bids(self, mock_bid_filter):
        """Verify response when auction is close and there are winners"""

        # Fake Bids Queryset
        bids_queryset = [FakeBid(False, 50), FakeBid(False, 60), FakeBid(False, 20)]

        mock_aggregate = MagicMock()
        mock_aggregate.aggregate.return_value = {"amount__sum": 110}
        mock_aggregate.order_by.return_value = bids_queryset
        mock_bid_filter.return_value = mock_aggregate

        data = {"status": "closed"}
        response = self.client.put(f"{self.endpoint}{self.auction1.id}", data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifies winners selected
        self.assertTrue(bids_queryset[0].winner)
        self.assertTrue(bids_queryset[1].winner)
        self.assertFalse(bids_queryset[2].winner)

        # Verifies that auction is close
        auction_result = Auction.objects.get(id=self.auction1.id)
        self.assertEqual(auction_result.status, Auction.OPT_STATUS_CLOSED)


class BidListCreateTest(TestCase):
    """Unit tests for listing and creating bids using endpoints"""

    def setUp(self):
        # User for testing
        self.user = User(username="user_test1")
        self.user.save()

        # Create auctions and bids for testing proposes
        self.auction1 = Auction(amount=100)
        self.auction2 = Auction(amount=200)
        self.auction1.save()
        self.auction2.save()
        bids = [
            Bid(user=self.user, auction=self.auction1, amount=40, discount_rate=1.0),
            Bid(user=self.user, auction=self.auction2, amount=30, discount_rate=1.1)
        ]
        Bid.objects.bulk_create(bids)

        self.client = APIClient()

    def test_methods_not_allowed(self):
        """Verify error response when client uses methods not allowed"""
        pass

    def test_getting_all_bids(self):
        """Verify response when client requests for bids"""
        pass

    def test_check_creation_error_when_id(self):
        """Verify error when client tries to create a bid with id"""
        pass

    def test_check_creation_error_when_status_closed(self):
        """Verify error when client tries to create a bid with auction status closed"""
        pass

    def test_when_creation_serializer_validation_is_not_correct(self):
        """Verify error when serializer validation raise an error during creation"""
        pass

    def test_when_creation_request_is_correct(self):
        """Verify correct creation"""
        pass
