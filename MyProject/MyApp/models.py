from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager



# Replace 'your_username', 'your_password', and 'your_database_name' with actual values


# engine = create_engine('postgresql://postgresql:root123@localhost/socail_book')
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True, default="Default")
    email = models.EmailField(unique=True)
    public_visibility = models.BooleanField(default=True)
    age = models.IntegerField(null=True, blank=True)
    birth_year = models.PositiveIntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class UploadedFile(models.Model):
    user_id = models.IntegerField(null=True)
    title = models.CharField(max_length=255)
    visibility = models.BooleanField(default=True)
    description = models.CharField(max_length=500)
    cost = models.IntegerField()
    year_of_published = models.IntegerField()
    file = models.FileField(upload_to='books/', default=None)
    uploaded_at = models.DateTimeField(auto_now_add=True)

