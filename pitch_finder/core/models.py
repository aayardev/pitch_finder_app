"""
Database models.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

import re


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        email = self.normalize_email(email)
        username = self.generate_username(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    def generate_username(self, email):
        username = email.split("@")[0]
        username = re.sub("[^a-zA-Z0-9_]", "_", username)
        return username


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."  # noqa
        ),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("Prénom"), max_length=255, null=True, blank=True)
    last_name = models.CharField(_("Nom"), max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return self.first_name.capitalize() + " " + self.last_name

        return ""


class Pitch(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Reservation(models.Model):

    class Slot(models.TextChoices):
        """Slots for the reservation."""

        _8TO9 = "8to9", "8am-9am"
        _9TO10 = "9to10", "9am-10am"
        _10TO11 = "10to11", "10am-11am"
        _11TO12 = "11to12", "11am-12pm"
        _2TO3 = "2to3", "2pm-3pm"
        _3TO4 = "3to4", "3pm-4pm"
        _4TO5 = "4to5", "4pm-5pm"
        _5TO6 = "5to6", "5pm-6pm"
        _6TO7 = "6to7", "6pm-7pm"
        _7TO8 = "7to8", "7pm-8pm"
        _8TO9_PM = "8to9pm", "8pm-9pm"
        _9TO10_PM = "9to10_pm", "9pm-10pm"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pitch = models.ForeignKey(Pitch, on_delete=models.CASCADE)
    time = models.CharField(
        max_length=20,
        choices=Slot.choices,
        default=Slot._8TO9,
    )
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.user.username} reserved {self.reservation_time} on {self.pitch}"  # noqa
