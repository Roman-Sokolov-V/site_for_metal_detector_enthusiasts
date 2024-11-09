import django.db.models
from django.contrib.auth.models import AbstractUser
from django.db import models
from my_precious.settings import AUTH_USER_MODEL



RATING_CHOICES = [(1, 1),(2, 2),(3, 3),(4, 4), (5, 5)]

class User(AbstractUser):
    detector_model = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ("username",)

    def __str__(self):
        return self.username


class Finding(models.Model):
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    date_found = models.DateField(blank=True, null=True)
    rating = models.IntegerField(null=True, blank=True, choices=RATING_CHOICES)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="findings")
    collections = models.ManyToManyField("Collection", related_name="findings", blank= True)
    created_at = models.DateTimeField(auto_now_add=True,)

    class Meta:
        verbose_name = "Finding"
        verbose_name_plural = "Findings"
        ordering = ("-date_found", "-rating")

    def __str__(self):
        return f"{self.name}"


class Collection(models.Model):
    name = models.CharField(max_length=255, blank=True, unique = True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Collection"
        verbose_name_plural = "Collections"
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"

class Image(models.Model):
    finding = models.ForeignKey(Finding, on_delete=models.CASCADE, related_name="images")
    image_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return f"'{self.finding.name}' id: {self.pk}"



class Feedback(models.Model):
    reviewer = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviewers")
    comment = models.TextField(blank=True, null=True)
    finding = models.ForeignKey(Finding, on_delete=models.CASCADE, related_name="feedbacks")
    rating = models.IntegerField(choices=RATING_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        ordering = ("-created_at",)

    def __str__(self):
        return f"'{self.finding.name}' feedback by {self.reviewer.username}"