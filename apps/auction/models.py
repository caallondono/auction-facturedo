from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class Auction(models.Model):
    """Model to manage auctions data"""

    OPT_STATUS_OPEN = "open"
    OPT_STATUS_CLOSED = "closed"

    LIST_OPT_STATUS = [OPT_STATUS_OPEN, OPT_STATUS_CLOSED]

    CHOICES_STATUS =(
        (OPT_STATUS_OPEN, "Open Status"),
        (OPT_STATUS_CLOSED, "Close Status")
    )

    amount = models.FloatField(
        validators=[MinValueValidator(1)],
        default=1,
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
        ordering = ['id']
        verbose_name = "Auction"
        verbose_name_plural = "Auctions"

    def __str__(self):
        return f"Id: {self.id} - Amount: {self.amount}"


class Bid (models.Model):
    """Model to manage user bid data. Each bid is related to an auction"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    amount = models.FloatField(
        validators=[MinValueValidator(1)],
        default=1,
        verbose_name="Bid amount"
    )

    discount_rate = models.FloatField(
        verbose_name="Discount Rate",
        help_text="Criteria for selecting winners bids. If it's lower, it increases the chances"
    )

    winner = models.BooleanField(
        default=False,
        verbose_name="Winner Bid?",
        help_text="Is this a winner bid?"
    )

    class Meta:
        ordering = ['id']
        verbose_name = "Bid"
        verbose_name_plural = "Bids"

    def __str__(self):
        return f"Auction: [{self.auction.id}][{self.auction.amount}] - Amount: {self.amount} - Winner: {self.winner}"
