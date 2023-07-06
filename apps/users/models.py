import logging

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from apps.products.models import ProductProvider
from config.mixins import TimestampMixin

logger = logging.getLogger("rapport")


class UserManager(BaseUserManager):
    """
    Custom account model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    use_in_migrations = True

    def create_user(
        self,
        email=None,
        password=None,
        **extra_fields,
    ):
        """
        Create and save a User with the given email and password.
        """
        extra_fields.setdefault("is_superuser", False)

        if not email:
            raise ValueError("Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)
        logger.info(f"User [{user.id}] 회원가입")
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractBaseUser, TimestampMixin, PermissionsMixin):
    email = models.EmailField(max_length=64, unique=True, null=False)
    name = models.CharField(max_length=10, null=False)
    affiliation = models.CharField(
        max_length=10, null=False, choices=ProductProvider.choices
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        db_table = "user"

    def __str__(self):
        return f"[{self.id}] {self.email}"

    def __repr__(self):
        return f"User({self.id}, {self.email})"


class UserRefreshToken(TimestampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    token = models.CharField(max_length=300, null=False)

    class Meta:
        db_table = "user_refresh_token"

    def __str__(self):
        return f"[{self.id}] {self.user}"

    def __repr__(self):
        return f"RefreshToken({self.user})"
