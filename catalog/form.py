from email.policy import default

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


from catalog.models import User, Finding, Image, Feedback


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("detector_model",)


class UserSerchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
    )


class FindingCreationForm(forms.ModelForm):
    class Meta:
        model = Finding
        fields = "__all__"
        widgets = {"user": forms.HiddenInput(),}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['user'].initial = user
            self.fields["user"].disabled = True























class FindingSerchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = "__all__"

        widgets = {
            "reviewer": forms.HiddenInput(),
            "finding": forms.HiddenInput(),
            "comment": forms.TextInput(
                attrs={
                    "placeholder": "Add a comment",
                   # "size": "40"
                },

            ),
        }
        labels = {
            "comment": "",
            "rating": "Rate",
        }