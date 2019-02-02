from itertools import chain

from django.contrib.auth.models import User
from django.test import TestCase
from mock import patch

from apps.auction.models import Auction, Bid
from apps.auction.serializers import AuctionSerializer, BidSerializer


class FakeMethodContext:
    method = "PUT"

    def method(self):
        return self.method


class AuctionSerializersTest(TestCase):
    """Unit tests for Serializers"""

    def setUp(self):
        data_auction = {"id": 1, "amount": 1000}
        self.auction = Auction(**data_auction)
        self.serializer_auction = AuctionSerializer(self.auction)

    def test_contain_expected_fields(self):
        """Verify that serializer returns correct keys"""
        data = self.serializer_auction.data
        self.assertEqual(set(data.keys()), {'amount', 'id', 'status'})

    def test_validator_correct_data(self):
        """Verify serializer validation in a correct scenario"""
        data_auction = {"id": 1, "amount": 1000}
        self.serializer = AuctionSerializer(data=data_auction)
        self.assertTrue(self.serializer.is_valid())

    def test_validator_serializer_when_status_closed(self):
        """Verify serializer validation when auction status is closed"""
        data_auction = {"id": 1, "amount": 1000, "status": "closed"}
        self.serializer = AuctionSerializer(data=data_auction)
        fake_context = FakeMethodContext()
        self.serializer.context["request"] = fake_context
        self.assertFalse(self.serializer.is_valid())


class BidSerializersTest(TestCase):
    """Unit tests for Serializers"""

    def setUp(self):
        data_user = {"id": 1, "username": "user1_test"}
        self.user = User(**data_user)
        self.user.save()

        data_auction = {"id": 1, "amount": 1000}
        self.auction = Auction(**data_auction)
        self.auction.save()

        self.data_bid = {"id": 1, "user": self.user, "auction": self.auction, "amount": 100, "discount_rate": 1}
        self.bid = Bid(**self.data_bid)
        self.serializer_bid = BidSerializer(self.bid)

    def test_contain_expected_fields(self):
        """Verify that serializer returns correct keys"""
        data = self.serializer_bid.data
        self.assertEqual(set(data.keys()), {
            'id',
            'amount',
            'auction_id',
            'auction_amount',
            'winner',
            'discount_rate',
            'username'
        })

    def test_validator_correct_data(self):
        """Verify serializer validation in a correct scenario"""
        data_bid = {"id": 1, "user": 1, "auction": 1, "amount": 100, "discount_rate": 1}
        serializer = BidSerializer(data=data_bid)
        resp = serializer.is_valid()
        self.assertTrue(resp)

    @patch('apps.auction.models.Bid.objects.filter')
    def test_validator_when_bids_amount_greater_than_auction_amount(self, mock_bid_filter):
        """Verify serializer validation when bids amount is greater than auction amount"""
        fake_queryset = [{"id": 1}, {"id": 2}]
        mock_bid_filter.return_value = fake_queryset

        data_bid = {"id": 1, "user": self.user.id, "auction": self.auction.id, "amount": 100, "discount_rate": 1}
        serializer = BidSerializer(data=data_bid)
        self.assertFalse(serializer.is_valid())

    def test_validator_when_winner_true(self):
        """Verify serializer validation when winner field is true"""
        data_bid = {
            "id": 1,
            "user": self.user.id,
            "auction": self.auction.id,
            "amount": 100,
            "discount_rate": 1,
            "winner": True
        }
        serializer = BidSerializer(data=data_bid)
        self.assertFalse(serializer.is_valid())
