from django.apps import apps
from django.test import TestCase
from apps.auction.apps import AuctionConfig


class AuctionConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(AuctionConfig.name, 'auction')
        self.assertEqual(apps.get_app_config('auction').name, 'apps.auction')
