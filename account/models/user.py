from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..utils import GroupPermission
from .user_manager import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_("Email"), unique=True)
    username = models.CharField(verbose_name=_("Username"), max_length=100)
    is_staff = models.BooleanField(verbose_name=_("Is Staff"), default=True)
    is_active = models.BooleanField(verbose_name=_("Is Active"), default=False)
    phone_number = models.CharField(verbose_name=_("Phone Number"), max_length=12)
    profile_picture = models.ImageField(
        verbose_name=_("Profile Picture"), upload_to="profile_picture", null=True, blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number", "username"]

    objects = CustomUserManager()

    class Meta:
        ordering = ("id",)
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.email

    @property
    def role(self):
        group = self.groups.first()
        return group.name if group else None

    @property
    def is_adminuser(self):
        permission = GroupPermission(self, "Admin")
        return permission._has_group_permission()

    @property
    def is_facultyuser(self):
        permission = GroupPermission(self, "Faculty")
        return permission._has_group_permission()

    @property
    def is_subscribedfacultyuser(self):
        permission = GroupPermission(self, "Subscribed Faculty")
        return permission._has_group_permission()

    @property
    def is_studentuser(self):
        permission = GroupPermission(self, "Student")
        return permission._has_group_permission()

    @property
    def is_subscribedstudentuser(self):
        permission = GroupPermission(self, "Subscribed Student")
        return permission._has_group_permission()
