from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def get_or_create_for_cognito(self, payload):
        cognito_id = payload['sub']
        print(payload)
        try:
            return self.get(cognito_id=cognito_id)
        except self.model.DoesNotExist:
            pass

        try:
            user = self.create(
                cognito_id=cognito_id,
                email=payload['email'],
                username=payload['cognito:username'],
                phone_number=payload['phone_number'],
                is_active=True,
                is_staff = True
                )
        except IntegrityError:
            user = self.get(cognito_id=cognito_id)

        return user
    
    def create_user(self, email, password, role, **extra_fields):
        """
        Create and save a user with the given email and password and assign given role.
        """
        
        if not Group.objects.filter(name=role).exists():
            raise Exception(f"Please run create_groups command first for group create for {role} role")

        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        user.groups.add(get_object_or_404(Group, name__iexact=role))
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        self.create_user(email, password, 'Admin', **extra_fields)