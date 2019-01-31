from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class Auction(models.Model):
    """Model to manage auctions data"""

    OPT_STATUS_OPEN = "open"
    OPT_STATUS_CLOSED = "closed"

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
        verbose_name = "Auction"
        verbose_name_plural = "Auctions"

    def __str__(self):
        return f"ID: {self.id} - Amount: {self.amount}"


class Bid (models.Model):
    """Model to manage user bid data. Each bid is related to an auction"""

    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    amount = models.FloatField(
        validators=[MinValueValidator(1)],
        default=1,
        verbose_name="Bid amount"
    )

    discount_rate = models.FloatField(
        verbose_name="Discount Rate",
        help_text="Criteria for selecting winners bids. If it's lower, it's better"
    )

    winner = models.BooleanField(
        default=False,
        verbose_name="Winner Bid?",
        help_text="Is this a winner bid?"
    )

    class Meta:
        verbose_name = "Bid"
        verbose_name_plural = "Bids"

    def __str__(self):
        return f"ID: {self.id} - Amount: {self.amount} - Winner: {self.winner}"
