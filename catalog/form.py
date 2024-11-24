from email.policy import default

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


from catalog.models import User, Finding, Image, Feedback, Collection


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
        widgets = {
            "user": forms.HiddenInput(),
            "name": forms.TextInput(attrs={"placeholder": "Name"}),
            "description": forms.Textarea(
                attrs={"placeholder": "Description"}
            ),
            "location": forms.TextInput(attrs={"placeholder": "Location"}),
            "date_found": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "name": "",
            "description": "",
            "location": "",
            "date_found": "",
            "collections": "",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["user"].initial = user
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
            "rating": forms.Select(
                attrs={
                    "class": "form-control w-auto",
                },
            ),
            "comment": forms.Textarea(
                attrs={
                    "placeholder": "Add a comment",
                    "cols": "2000",
                    "rows": "1",
                },
            ),
        }
        labels = {
            "comment": "",
            "rating": "",
        }


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = [
            "photo",
        ]
        widgets = {
            "photo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
        labels = {"photo": ""}

    def __init__(self, *args, finding=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.finding = finding
        if finding:
            self.fields["finding"].initial = finding
            self.fields["finding"].widget = forms.HiddenInput()
