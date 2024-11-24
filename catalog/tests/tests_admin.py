from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="<PASSWORD>"
        )
        self.client.force_login(self.admin_user)
        self.comrade = get_user_model().objects.create_user(
            username="comrade", password="<testPASSWORD>", detector_model="Quasar"
        )

    def test_user_detector_model_listed(self):
        url = reverse("admin:catalog_user_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.comrade.detector_model)

    def test_user_detail_detector_model_listed(self):
        url = reverse("admin:catalog_user_change", args=[self.comrade.id])
        res = self.client.get(url)
        self.assertContains(res, self.comrade.detector_model)

    def test_add_user_detail_detector_model_listed(self):
        url = reverse("admin:catalog_user_add")
        res = self.client.get(url)
        self.assertContains(res, "first_name")
        self.assertContains(res, "last_name")
        self.assertContains(res, "detector_model")
