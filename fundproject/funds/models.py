from django.db import models
from django.core.validators import MinValueValidator, MaxLengthValidator
import datetime
from decimal import Decimal

STRATEGY_CHOICES = [
    ('Long/Short Equity', 'Long/Short Equity'),
    ('Global Macro', 'Global Macro'),
    ('Arbitrage', 'Arbitrage'),
]  # If strategy choices needs to be limited to a finite set.


class Fund(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        validators=[MaxLengthValidator(255)],
        null=False,
        blank=False,
        help_text="Name of the fund. Must be unique and under 255 characters."
    )

    strategy = models.CharField(
        max_length=50,
        # choices=STRATEGY_CHOICES,

        help_text="Select a strategy from the predefined list."
    )

    aum = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Assets Under Management (in USD). Must be a positive value."
    )

    inception_date = models.DateField(
        help_text="Inception date of the fund (format: YYYY-MM-DD).",
        default=datetime.date.today()
    )

    def __str__(self):
        return f"{self.name} ({self.strategy})"
