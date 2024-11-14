from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


from catalog.models import User, Finding


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("detector_model",)


class FindingCreationForm(forms.ModelForm):
    rating = forms.FloatField()
    class Meta:
        model = Finding
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['user'].initial = user
            self.fields['user'].widget = forms.HiddenInput()
