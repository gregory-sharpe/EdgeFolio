from django.test import TestCase
from funds.models import Fund
from decimal import Decimal
import datetime
from django.core.exceptions import ValidationError
import unittest


class FundModelTests(TestCase):
    valid_name = "Test Fund A"
    valid_strategy = "Global Macro"
    valid_aum = 1.00
    valid_inception_date = datetime.date(2022, 1, 1)

    def test_valid_name(self):
        fund = Fund(
            name="Test Fund A",
            strategy="Global Macro",
            aum=Decimal("1000000.00"),
            inception_date=datetime.date(2022, 1, 1)
        )
        try:
            fund.full_clean()  # validates all model fields
        except ValidationError:
            self.fail("Valid name caused a ValidationError")

    def test_empty_name_invalid(self):
        fund = Fund(
            name="",
            strategy="Global Macro",
            aum=Decimal("1000000.00"),
            inception_date=datetime.date(2022, 1, 1)
        )
        with self.assertRaises(ValidationError, msg="Empty name should raise ValidationError"):
            fund.full_clean()

    def test_negative_aum_invalid(self):
        fund = Fund(
            name="Negative AUM Fund",
            strategy="Arbitrage",
            aum=Decimal("-500.00"),
            inception_date=datetime.date(2022, 1, 1)
        )
        with self.assertRaises(ValidationError, msg="Negative AUM should raise ValidationError"):
            fund.full_clean()

    def test_valid_strategy(self):
        fund = Fund(
            name="Valid Strategy Fund",
            strategy="Long/Short Equity",
            aum=Decimal("2000000.00"),
            inception_date=datetime.date(2023, 1, 1)
        )
        try:
            fund.full_clean()
        except ValidationError:
            self.fail("Valid strategy raised ValidationError")

    @unittest.skip("Optional test — only use when valid strategies become \
                   finite")
    def test_invalid_strategy(self):
        fund = Fund(
            name="Invalid Strategy Fund",
            strategy="Fake Strategy",
            aum=Decimal("100000.00"),
            inception_date=datetime.date(2023, 1, 1)
        )
        with self.assertRaises(ValidationError, msg="Invalid strategy should \
                               raise ValidationError"):
            fund.full_clean()

    def test_inception_date_defaults_to_today_timezone(self):
        """If you switched to default=timezone.now on a DateField, compare to \
              timezone.localdate()."""

        today_date = datetime.date.today()
        fund = Fund(
            name="DefaultDateFund2",
            strategy="Long/Short Equity",
            aum=Decimal("2000.00")
        )
        # before save, the default should already be set on the instance
        self.assertEqual(fund.inception_date, today_date,
                         msg=f"inception_date on instantiation was {fund.inception_date!r}, expected {today_date!r}")
        # and of course it stays the same once saved
        fund.save()
        self.assertEqual(fund.inception_date, today_date)

    def test_null_name_invalid(self):
        fund = Fund(
            name=None,
            strategy=self.valid_strategy,
            aum=self.valid_aum,
            inception_date=self.valid_inception_date
        )
        with self.assertRaises(ValidationError, msg="Null name should raise ValidationError"):
            fund.full_clean()

    def test_blank_name_invalid(self):
        fund = Fund(
            name="",
            strategy=self.valid_strategy,
            aum=self.valid_aum,
            inception_date=self.valid_inception_date
        )
        with self.assertRaises(ValidationError, msg="Blank name should raise ValidationError"):
            fund.full_clean()

    def test_null_strategy_invalid(self):
        fund = Fund(
            name=self.valid_name,
            strategy=None,
            aum=self.valid_aum,
            inception_date=self.valid_inception_date
        )
        with self.assertRaises(ValidationError, msg="Null strategy should raise ValidationError"):
            fund.full_clean()

    def test_blank_strategy_invalid(self):
        fund = Fund(
            name=self.valid_name,
            strategy="",
            aum=self.valid_aum,
            inception_date=self.valid_inception_date
        )
        with self.assertRaises(ValidationError, msg="Blank strategy should raise ValidationError"):
            fund.full_clean()

    def test_excessive_decimal_places_invalid(self):
        # 6 decimal places—your model only allows 2
        # Maybe decimal places should be rounded instead.
        fund = Fund(
            name="Bitcoin Fund",
            strategy=self.valid_strategy,
            aum=Decimal("1.123456"),
            inception_date=self.valid_inception_date
        )
        with self.assertRaises(ValidationError, msg="AUM with too many decimals should raise ValidationError"):
            fund.full_clean()

    def test_duplicate_name_invalid(self):
        # first one is fine
        Fund.objects.create(
            name="UniqueFund",
            strategy=self.valid_strategy,
            aum=self.valid_aum,
            inception_date=self.valid_inception_date

        )
        # second with same name should fail unique check
        dup = Fund(
            name="UniqueFund",
            strategy=self.valid_strategy,
            aum=self.valid_aum,
            inception_date=self.valid_inception_date
        )
        with self.assertRaises(ValidationError, msg="Duplicate name should raise ValidationError"):
            dup.full_clean()
