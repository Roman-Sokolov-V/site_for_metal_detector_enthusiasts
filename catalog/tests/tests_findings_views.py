from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from  django.urls import reverse, reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile

from catalog.models import Collection, Finding, Feedback, Image
from catalog.form import FindingSerchForm, FeedbackForm, FindingCreationForm


class TestFindingsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="<PASSWORD123>",
        )
        self.collection = Collection.objects.create(name="gold", description="some text")
        self.finding = Finding.objects.create(name="gold", user=self.user)
        self.finding.collections.add(self.collection)

    def test_get_context_data(self):
        url = reverse("catalog:findings")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(response.context["search_form"], FindingSerchForm)

class FindingsDetailViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="<PASSWORD123>",
        )
        self.collection = Collection.objects.create(name="gold", description="text")
        self.finding = Finding.objects.create(name="gold", user=self.user)
        self.finding.collections.add(self.collection)
        self.another_finding = Finding.objects.create(name="silver", user=self.user)
        self.finding.collections.add(self.collection)

    def test_get_context_data(self):
        url = reverse("catalog:findings-detail", kwargs={"pk": self.finding.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("feedback_form", response.context)
        self.assertIsInstance(response.context["feedback_form"], FeedbackForm)
        self.assertIn("average_rating", response.context)

    def test_post_valid_feedback(self):
        url = reverse("catalog:findings-detail", kwargs={"pk": self.finding.pk})
        # Валідні дані для форми

        valid_data = {
            "reviewer": self.user.id,
            "finding": self.finding.id,
            "rating": 4,
            "comment": "Great finding!",
        }
        valid_data["submit_feedback"] = "Submit"
        response = self.client.post(url, data=valid_data,)
        self.assertRedirects(
            response,
            reverse("catalog:findings-detail", kwargs={"pk": self.finding.pk}),
        )
        valid_data.pop("submit_feedback")
        self.assertTrue(Feedback.objects.filter(**valid_data).exists())

    def test_post_invalid_feedback(self):
        url = reverse("catalog:findings-detail", kwargs={"pk": self.finding.pk})
        invalid_data = {
            "reviewer": self.user.id,
            "finding": self.finding.id,
            "comment": "Invalid rating",
            "rating": 10,
        }
        invalid_data["submit_feedback"] = "Submit"
        response = self.client.post(url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("feedback_form", response.context)
        form = response.context["feedback_form"]
        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)
        invalid_data.pop("submit_feedback")
        self.assertFalse(Feedback.objects.filter(**invalid_data).exists())

    def test_post_valid_add_image(self):
        url = reverse("catalog:findings-detail", kwargs={"pk": self.finding.pk})
        with open("catalog/static/test_images/test.jpg", "rb") as img:
            test_image = SimpleUploadedFile(
                name="test.jpg",
                content=img.read(),
                content_type="image/jpeg"
            )
        valid_data = {
            "finding": self.finding.id,
            "photo": test_image,
        }
        valid_data["submit_image"] = "Submit"
        response = self.client.post(url, data=valid_data, )
        self.assertRedirects(
            response,
            reverse("catalog:findings-detail", kwargs={"pk": self.finding.pk}),
        )
        valid_data.pop("submit_image")
        self.assertTrue(Image.objects.filter(**valid_data).exists())

    def test_post_invalid_feedback(self):
        url = reverse("catalog:findings-detail", kwargs={"pk": self.finding.pk})
        invalid_data = {
            "reviewer": self.user.id,
            "finding": self.finding.id,
            "comment": "Invalid rating",
            "rating": 10,
        }
        invalid_data["submit_feedback"] = "Submit"
        response = self.client.post(url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("feedback_form", response.context)
        form = response.context["feedback_form"]
        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)
        invalid_data.pop("submit_feedback")
        self.assertFalse(Feedback.objects.filter(**invalid_data).exists())

class FindingsCreateViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="<PASSWORD123>",
        )

    def test_user_is_not_authenticated(self):
        url = reverse("catalog:findings-create")
        data = {
            "name": "Gold",
            "user": self.user.pk,
        }
        response = self.client.post(url, data=data)
        self.assertNotEqual(response.status_code, 200)
        self.assertFalse(Finding.objects.filter(**data).exists())

    def test_user_is_authenticated(self):
        self.client.force_login(self.user)
        url = reverse("catalog:findings-create")
        data = {
            "name": "Gold",
            "user": self.user.pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse_lazy("catalog:findings")
        )
        self.assertTrue(Finding.objects.filter(**data).exists())
