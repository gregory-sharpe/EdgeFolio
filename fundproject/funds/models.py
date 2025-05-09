from django.db import models
from django.core.validators import MinValueValidator, MaxLengthValidator
from decimal import Decimal
from django.utils import timezone
# from utils.flags import potential_performance_flag
STRATEGY_CHOICES = [  # Should be in another file
    ('Long/Short Equity', 'Long/Short Equity'),
    ('Global Macro', 'Global Macro'),
    ('Arbitrage', 'Arbitrage'),
    ("Event-Driven", "Event-Driven"),
    ("Quantitative", "Quantitative"),
    ("Distressed Securities", "Distressed Securities"),
    ("Multi-Strategy", "Multi-Strategy"),
    ("Credit", "Credit"),
    ("Fixed Income Arbitrage", "Fixed Income Arbitrage"),
    ("Market Neutral", "Market Neutral"),
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
        choices=STRATEGY_CHOICES,  # comment out if strategies is not finite.
        help_text="Select a strategy from the predefined list."
    )

    aum = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Assets Under Management (in USD). Must be a positive value."
    )
    # TODO test for rounding errors

    inception_date = models.DateField(
        help_text="Inception date of the fund (format: YYYY-MM-DD).",
        default=timezone.localdate  # probably causes localisation issues
    )

    def __str__(self):
        return f"{self.name} ({self.strategy})"


# #    @potential_performance_flag
#     def save(self, *args, **kwargs):
#         # The assumption is that perfomance is not an issue.
#         # overwrites save so data is always validated.

#         self.full_clean()
#         super().save(*args, **kwargs)
#         n
