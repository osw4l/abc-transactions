from django.contrib import admin

from apps.datos.forms import CustomUserCreationForm
from .models import CustomUser, Transaction
# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'email',
        'birth_date'
    ]
    form = CustomUserCreationForm


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'created_at',
        'value',
        'points',
        'status'
    ]
