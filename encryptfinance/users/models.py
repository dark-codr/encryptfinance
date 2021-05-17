from __future__ import absolute_import

import os
import uuid
import random
import datetime

from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db.models import (
    CharField,
    ForeignKey,
    OneToOneField,
    EmailField,
    DateTimeField,
    CASCADE,
    BooleanField,
    DecimalField,
    FileField,
    UUIDField,
    URLField,
    DateField,
)
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


from model_utils.models import TimeStampedModel
from countries_plus.models import Country


from ..utils.validators import (
    validate_uploaded_image_extension,
    validate_uploaded_pdf_extension,
)


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def idcard_image(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "idcard/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )


def profile_image(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "profile/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )


def bank_statement(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "statement/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )


SSN_REGEX = "^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4}\\d{4}$)"
NUM_REGEX = "^[0-9]*$"


class User(AbstractUser):
    """Default user for encryptfinance."""

    #: First and last name do not cover name patterns around the globe
    middle_name = CharField(
        _("Middle Name"), blank=True, null=True, max_length=255, help_text="Not compulsary, But good practive to differentciate owners"
    )
    balance = DecimalField(_("Current Balance"), max_digits=20, null=True, decimal_places=2, default=0.00)
    unique_id = UUIDField(editable=False, default=uuid.uuid1)
    member_since = DateField(default=datetime.datetime.now)
    is_verified = BooleanField(default=False)
    has_deposited = BooleanField(default=False)
    deposit_date = DateField(default=datetime.datetime.now, null=True, blank=True)

    @property
    def plan(self):
        if self.balance > 0.00 and self.balance <= 1000.00:
            return "DAILY PLAN"
        elif self.balance > 1000.00 and self.balance <= 4000.00:
            return "SILVER PLAN"
        elif self.balance > 4000.00 and self.balance <= 50000.00:
            return "GOLD PLAN"
        elif self.balance > 50000.00 and self.balance <= 100000.00:
            return "DIAMOND PLAN"
        elif self.balance == 0.00:
            return "UNSUBSCRIBED"

    @property
    def rate(self):
        if self.plan == "DAILY PLAN":
            return 0.2
        elif self.plan == "SILVER PLAN":
            return 3
        elif self.plan == "GOLD PLAN":
            return 5
        elif self.plan == "DIAMOND PLAN":
            return 7
        elif self.plan == "UNSUBSCRIBED":
            return 0.00

    @property
    def days(self):
        if self.plan == "DAILY PLAN":
            return 1
        elif self.plan == "SILVER PLAN":
            return 14
        elif self.plan == "GOLD PLAN":
            return 60
        elif self.plan == "DIAMOND PLAN":
            return 90
        elif self.plan == "UNSUBSCRIBED":
            return 0


    def withdrawal_date(self):
        if self.plan == "BRONZE PLAN":
            days = 1
            if self.deposit_date:
                return self.deposit_date + datetime.timedelta(days=days)

        elif self.plan == "SILVER PLAN":
            days = 14
            if self.deposit_date:
                return self.deposit_date + datetime.timedelta(days=days)

        elif self.plan == "GOLD PLAN":
            days = 60
            if self.deposit_date:
                return self.deposit_date + datetime.timedelta(days=days)

        elif self.plan == "DIAMOND PLAN":
            days = 90
            if self.deposit_date:
                return self.deposit_date + datetime.timedelta(days=days)

        elif self.plan == "UNSUBSCRIBED":
            days = 0
            if self.deposit_date:
                return self.deposit_date + datetime.timedelta(days=days)

    def can_withdraw(self):
        if self.plan == "BRONZE PLAN":
            days = 1
            terminate_date = self.deposit_date + datetime.timedelta(days=days)
            if timezone.now().date() > terminate_date:
                return True

        elif self.plan == "SILVER PLAN":
            days = 14
            terminate_date = self.deposit_date + datetime.timedelta(days=days)
            if timezone.now().date() > terminate_date:
                return True

        elif self.plan == "GOLD PLAN":
            days = 60
            terminate_date = self.deposit_date + datetime.timedelta(days=days)
            if timezone.now().date() > terminate_date:
                return True

        elif self.plan == "DIAMOND PLAN":
            days = 90
            terminate_date = self.deposit_date + datetime.timedelta(days=days)
            if timezone.now().date() > terminate_date:
                return True

        elif self.plan == "UNSUBSCRIBED":
            days = 0
            terminate_date = self.deposit_date + datetime.timedelta(days=days)
            if timezone.now().date() > terminate_date:
                return False

    def profit(self):
        return self.balance + (self.balance * Decimal(self.rate))

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class UserProfile(TimeStampedModel):
    BANKS = (
        ("", "Select Bank"),
        ("Arvest Bank", "Arvest Bank"),
        ("Ally Financial", "Ally Financial"),
        ("American Express", "American Express"),
        ("Amarillos National Bank", "Amarillos National Bank"),
        ("Apple bank for Savings", "Apple bank for Savings"),
        ("Bank of Hawaii", "Bank of Hawaii"),
        ("Bank of Hope", "Bank of Hope"),
        ("Bank United", "Bank United"),
        ("BOA", "Bank of America"),
        ("Bank United", "Bank United"),
        ("Brown Brothers Harriman & Co", "Brown Brothers Harriman & Co"),
        ("Barclays", "Barclays"),
        ("BMO Harris Bank", "BMO Harris Bank"),
        ("Bank OZK", "Bank OZK"),
        ("BBVA Compass", "BBVA Compass"),
        ("BNP Paribas", "BNP Paribas"),
        ("BOK Financial Corporation", "BOK Financial Corporation"),
        ("Cathay Bank", "Cathay Bank"),
        ("Chartway Federal Credit Union", "Chartway Federal Credit Union"),
        ("Capital One", "Capital One"),
        ("Capital City Bank", "Capital City Bank"),
        ("Chase Bank", "Chase Bank"),
        ("Charles Schwab Corporation", "Charles Schwab Corporation"),
        ("CG", "CitiGroup"),
        ("Credit Suisse", "Credit Suisse"),
        ("Comerica", "Comerica"),
        ("CIT Group", "CIT Group"),
        ("CapitalCity Bank", "CapitalCity Bank"),
        ("Credit Union Page", "Credit Union Page"),
        ("Citizens Federal Bank", "Citizens Federal Bank"),
        ("Chemical Financial Corporation", "Chemical Financial Corporation"),
        ("Discover Financial", "Discover Finacial"),
        ("Deutsche Bank", "Deutsche Bank"),
        ("Douglas County Bank & Trust", "Douglas County Bank & Trust "),
        ("Dime Savings Bank of Williamsburgh", "Dime Savings Bank of Williamsburgh"),
        ("East West Bank", "East West Bank"),
        ("Flagster Bank", "Flagster Bank"),
        ("First National of Nebraska", "First National of Nebraska"),
        ("FirstBank Holding Co", "FirstBank Holding Co"),
        ("First Capital Bank", "First Capital Bank"),
        ("First Commercial Bank", "First Commercial Bank"),
        (
            "First Federal Savings Bank of Indiana",
            "First Federal Savings Bank of Indiana",
        ),
        ("First Guaranty Bank of Florida", "First Guaranty Bank of Florida"),
        ("First Line Direct", "First Line Direct"),
        ("First USA Bank", "First USA Bank"),
        ("Fifth Third Bank", "Fifth Third Bank"),
        ("First Citizens BancShares", "First Citizens BancShares"),
        ("Fulton Financial Corporation", "Fulton Financial Corporation"),
        ("First Hawaiian Bank", "First Hawaiian Bank"),
        ("First Horizon National Corporation", "First Horizon National Corporation"),
        ("Frost Bank", "Frost Bank"),
        ("First Midwest Bank", "First Midwest Bank"),
        ("Goldman Sachs", "Goldman Sachs"),
        ("Grandeur Financials", "Grandeur Financials"),
        ("HSBC Bank USA", "HSBC Bank USA"),
        ("Home BancShares Conway", "Home BancShares Conway"),
        ("Huntington Bancshares", "Huntington Bancshares"),
        ("Investors Bank", "Investors Bank"),
        ("Íntercity State Bank", "Íntercity State Bank"),
        ("KeyCorp", "KeyCorp"),
        ("MB Financial", "MB Financial"),
        ("Mizuho Financial Group", "Mizuho Financial Group"),
        ("Midfirst Bank", "Midfirst Bank"),
        ("M&T Bank", "M&T Bank"),
        ("MUFG Union Bank ", "MUFG Union Bank"),
        ("Morgan Stanley", "Morgan Stanley"),
        ("Northern Trust", "Northern Trust"),
        ("New  York Community Bank", "New York Community Bank"),
        ("Old National Bank", "Old National Bank"),
        ("Pacwest Bancorp", "Pacwest Bancorp"),
        ("Pinnacle Financial Partners", "Pinnacle Financial Partners"),
        ("PNC Financial Services", "PNC Financial Services"),
        ("Raymond James Financial", "Raymond James Financial"),
        ("RBC Bank", "RBC Bank"),
        ("Region Financial Corporation", "Region Financial Corporation"),
        ("Satander Bank", "Satander Bank"),
        ("Synovus Columbus", "Synovus Columbus"),
        ("Synchrony Financial", "Synchrony Financial"),
        ("Sterling Bancorp", "Sterling Bancorp"),
        ("Simmons Bank", "Simmons Bank"),
        ("South State Bank", "South State Bank"),
        ("Stifel St. Louise", "Stifel St. Louise"),
        ("Suntrust Bank", "Suntrust Bank"),
        ("TCF Financial Corporation", "TCF Financial Corporation"),
        ("TD Bank", "TD Bank"),
        ("The Bank of New York Mellon", "The Bank of New York Mellon"),
        ("Texas Capital Bank", "Texas Capital Bank"),
        ("UMB Financial Corporation", "UMB Financial Corporation"),
        ("Utrecht-America", "Utrecht-America"),
        ("United Bank", "United Bank"),
        ("USAA", "USAA"),
        ("U.S Bank", "U.S Bank"),
        ("UBS", "UBS"),
        ("Valley National Bank", "Valley National Bank"),
        ("Washington Federal", "Washington Federal"),
        ("Western Alliance Banorporation", "Western Alliance Bancorporation"),
        ("Wintrust Financial", "Wintrust Finacial"),
        ("Webster Bank", "Webster Bank"),
        ("Wells Fargo", "Wells Fargo"),
        ("Zions Bancorporation", "Zions Bancorporation"),
        ("Other Bank", "Other Bank"),
    )
    user = OneToOneField(to=User, on_delete=CASCADE, related_name="userprofile")
    passport = FileField(
        _("User Profile Passport"),
        upload_to=profile_image,
        validators=[validate_uploaded_image_extension],
        null=True,
        blank=False,
    )

    bank = CharField(
        _("Your Bank Name"), max_length=250, blank=True, null=True, choices=BANKS
    )
    account_no = CharField(
        _("Recipient Account Number"),
        max_length=13,
        null=True,
        blank=False,
        validators=[
            RegexValidator(
                regex=NUM_REGEX,
                message="Must Contain Numbers Only",
                code="Invalid_input, Only Integers",
            )
        ],
    )
    routing_no = CharField(
        _("Recipient Routing Number"),
        max_length=13,
        null=True,
        blank=True,
        help_text="must be the recipients 9 digits routing number",
        validators=[
            RegexValidator(
                regex=NUM_REGEX,
                message="Must Contain Numbers Only",
                code="Invalid_input, Only Integers",
            )
        ],
    )
    nationality = ForeignKey(to=Country, on_delete=CASCADE, null=True)
    phone = CharField(
        _("Contact 10 digit Phone Number"),
        max_length=10,
        null=True,
        blank=True,
        unique=True,
        help_text="Example: 1234567890 (10 digits only)",
        validators=[
            RegexValidator(
                regex=NUM_REGEX,
                message="Must Contain Numbers Only",
                code="Invalid_input, Only Integers",
            )
        ],
    )

    @property
    def country_code(self):
        if self.nationality:
            country_code = self.nationality.phone
            return country_code

    def international_number(self):
        return f"{self.country_code}{self.phone}"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ["-modified"]

    def __str__(self):
        return (
            self.user.username
            if self.user.get_full_name() == ""
            else self.user.get_full_name()
        )



class UserVerify(TimeStampedModel):
    PASSPORT = "PASSPORT"
    ID_CARD = "ID_CARD"
    DRIVERS_LICENSE = "DRIVERS_LICENSE"
    ID_TYPE = (
        (PASSPORT, "PASSPORT"),
        (ID_CARD, "ID CARD"),
        (DRIVERS_LICENSE, "DRIVERS LICENSE"),
    )

    user = OneToOneField(to=User, on_delete=CASCADE, related_name="userverify")
    id_type = CharField(
        choices=ID_TYPE, default=PASSPORT, max_length=15, null=True, blank=True
    )
    id_front = FileField(
        _("ID Card Front"),
        upload_to=idcard_image,
        validators=[validate_uploaded_image_extension],
        null=True,
        blank=False,
        help_text="Must be SVG, PNG or JPG files",
    )
    id_back = FileField(
        _("ID Card Back"),
        upload_to=idcard_image,
        validators=[validate_uploaded_image_extension],
        null=True,
        blank=False,
        help_text="Must be SVG, PNG or JPG files",
    )
    bank_statement = FileField(
        _("Last 4 Months Bank Statement"),
        validators=[validate_uploaded_pdf_extension],
        upload_to=bank_statement,
        null=True,
        blank=True,
        help_text="Must be PDF or JPG files",
    )
    ssn = CharField(
        _("US SSN"),
        max_length=16,
        null=True,
        blank=True,
        unique=True,
        help_text="Must be valid Social Security Number. *** US Citizens Only",
        validators=[
            RegexValidator(
                regex=NUM_REGEX,
                message="Must Contain Numbers Only",
                code="Invalid_input, Only Integers",
            )
        ],
    )

    class Meta:
        verbose_name = "User Verify"
        verbose_name_plural = "User Verifies"
        ordering = ["-modified"]

    def __str__(self):
        return (
            self.user.username
            if self.user.get_full_name() == ""
            else self.user.get_full_name()
        )
