from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, AbstractUser
from django.utils.translation import gettext_lazy as _
from .user_manager import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=_("Email"),
        unique=True
    )
    username = models.CharField(
        verbose_name=_("Username"),
        max_length=100
    )
    is_staff = models.BooleanField(
        verbose_name=_("Is Staff"),
        default=True
    )
    is_active = models.BooleanField(
        verbose_name=_("Is Active"),
        default=False
    )
    phone_number = models.CharField(
        verbose_name=_("Phone Number"),
        max_length=12
    )
    profile_picture = models.ImageField(
        verbose_name=_("Profile Picture"),
        upload_to="profile_picture",
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'username']

    objects = CustomUserManager()

    class Meta:
        ordering = ('id',)
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.email
    

    @property
    def role(self):
        group = self.groups.first()
        return group.name if group else None


