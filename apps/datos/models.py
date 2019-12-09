from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from apps.datos.managers import UserManager
from .constants import ACTIVE, INACTIVE
# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(
        max_length=32,
        unique=True,
        primary_key=True,
        editable=False,
        blank=True
    )
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=254, null=True, blank=True)
    last_name = models.CharField(max_length=254, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    created_at = models.DateField(
        auto_now_add=True
    )
    birth_date = models.DateField(
        blank=True,
        null=True
    )
    username = models.CharField(
        max_length=40,
        blank=True,
        null=True
    )
    customuser = True

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

    def get_full_name(self):
        return '{} {}'.format(
            self.first_name,
            self.last_name
        )

    def get_points(self):
        return sum([
           t.points for t in Transaction.objects.filter(user=self, status=ACTIVE)
        ])


class Transaction(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True
    )
    created_at = models.DateField(
        auto_now_add=True
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    points = models.PositiveIntegerField()
    status = models.BooleanField(
        default=ACTIVE
    )

    def disable_transaction(self):
        self.status = INACTIVE
        self.save(update_fields=[
            'status'
        ])




