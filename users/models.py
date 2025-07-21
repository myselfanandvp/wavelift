from uuid import uuid4
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class User(AbstractUser,PermissionsMixin):

    id = models.UUIDField(_('User ID'), default=uuid4, primary_key=True, editable=False)
    username = models.CharField(_('User Name'), max_length=150, null=True, blank=True, default=None)
    email = models.EmailField(_('Email Address'), unique=True, blank=False, null=False)

    phone_number = models.CharField(
        max_length=13,
        unique=True,
        null=True,
        blank=False,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{9,13}$',
                message="Phone number must be in the format +910000000000. Up to 13 digits allowed."
            )
        ]
    )
    


    profile_img = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    class Roles(models.TextChoices):
        ADMIN = 'admin', 'ADMIN'
        STAFF = 'staff', 'STAFF'
        USER = 'user', 'USER'

    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.USER
    )

    class ActiveStatus(models.TextChoices):
        ACTIVE = 'active', 'ACTIVE'
        INACTIVE = 'inactive', 'INACTIVE'

    status = models.CharField(
        max_length=10,
        choices=ActiveStatus.choices,
        default=ActiveStatus.ACTIVE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'  # Use email to log in
    REQUIRED_FIELDS = ['username']  # Required when using createsuperuser

    def __str__(self):
        return f"{self.username} ({self.email})"

    def is_admin(self):
        return self.role == self.Roles.ADMIN

    def is_staff_user(self):
        return self.role == self.Roles.STAFF

    def is_normal_user(self):
        return self.role == self.Roles.USER
    

    
    
    class Meta:
        
        db_table="users"