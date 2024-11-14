from django.contrib.auth.forms import UserCreationForm
from catalog.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("detector_model",)