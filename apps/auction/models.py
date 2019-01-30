from django.db import models


class Auction(models.Model):

    OPT_STATUS_OPEN = "open"
    OPT_STATUS_CLOSED = "closed"

    CHOICES_STATUS =(
        (OPT_STATUS_OPEN, "Open Status"),
        (OPT_STATUS_CLOSED, "Close Status")
    )

    amount = models.FloatField(
        default=0,
        verbose_name="Amount"
    )

    status = models.CharField(
        max_length=10,
        default=OPT_STATUS_OPEN,
        choices=CHOICES_STATUS,
        verbose_name="Status",
        help_text="If it's switched to closed, we must to choose the winners bids"
    )

    class Meta:
        verbose_name = "Auction"
        verbose_name_plural = "Auctions"

    def __str__(self):
        return f"ID: {self.id} - Amount: {self.amount}"


class Bid (models.Model):

    amount = models.FloatField(
        verbose_name="",
        help_text=""
    )

    discount_rate = models.IntegerField(
        verbose_name="",
        help_text=""
    )

    winner = models.BooleanField(
        verbose_name="",
        help_text=""
    )

    class Meta:
        verbose_name = "Bid"
        verbose_name_plural = "Bids"

    def __str__(self):
        return f"ID: {self.id} - Amount: {self.amount}"
