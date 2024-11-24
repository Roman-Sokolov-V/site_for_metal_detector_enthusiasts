from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy

from catalog.models import Collection, Finding, Feedback
from catalog.form import FindingSerchForm, FeedbackForm, FindingCreationForm


class FeedbackViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="<PASSWORD123>",
        )
        self.finding = Finding.objects.create(name="gold", user=self.user)
        self.another_finding = Finding.objects.create(
            name="silver",
            user=self.user
        )
        self.feedback = Feedback.objects.create(
            comment="Gold", reviewer=self.user, finding=self.finding
        )
        self.another_feedback = Feedback.objects.create(
            comment="Silver", reviewer=self.user, finding=self.another_finding
        )

    def test_feedbacks_to_finding_view(self):
        url = reverse("catalog:feedbacks", kwargs={"pk": self.finding.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.feedback.comment)
        self.assertNotContains(response, self.another_feedback.comment)
