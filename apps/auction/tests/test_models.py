from django.contrib.auth.models import User
from django.test import TestCase

from apps.auction.models import Auction, Bid


class AuctionModelTest(TestCase):
    """Unit tests for Auction model"""

    def setUp(self):
        """Creating Auction instance for testing. No saving actions on DB"""
        self.auction_data = {
            "id": 1,
            "amount": 100
        }
        self.auction_test = Auction(**self.auction_data)

    def test_str_return_correctly(self):
        """Verifies if __str__ method works correctly"""
        expected = f"Id: {self.auction_data.get('id')} - Amount: {self.auction_data.get('amount')}"
        self.assertEqual(str(self.auction_test), expected)

    def test_status_is_open_in_creation(self):
        """Verify that status field is set correctly"""
        expected = "open"
        self.assertEqual(self.auction_test.status, expected)


class BidModelTest(TestCase):
    """Unit tests for Bid model"""

    def setUp(self):
        """Creating Bid instance for testing. No saving actions on DB"""
        user_data = {
            "username": "username1",
            "email": "email1@test.com"
        }
        user_test = User(**user_data)

        auction_data = {
            "id": 1,
            "amount": 100
        }
        self.auction_test = Auction(**auction_data)

        self.fake_data = {
            "id": 1,
            "user": user_test,
            "auction": self.auction_test,
            "amount": 100
        }
        self.bid_test = Bid(**self.fake_data)

    def test_str_return_correctly(self):
        """Verifies if __str__ method works correctly"""
        expected = f"Auction: {self.auction_test.amount} - Amount: {self.bid_test.amount} - DR: {self.bid_test.discount_rate} - Winner: {self.bid_test.winner}"
        self.assertEqual(str(self.bid_test), expected)

    def test_winner_is_false_in_creation(self):
        """Verify that winner field is set correctly"""
        self.assertFalse(self.bid_test.winner)
