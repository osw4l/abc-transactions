from apps.utils.forms import BaseUserCreationForm
from .models import CustomUser


class CustomUserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = CustomUser

