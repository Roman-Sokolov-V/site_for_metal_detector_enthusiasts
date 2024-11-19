from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from  django.urls import reverse, reverse_lazy


from catalog.models import Collection, Finding


class CollectionCreateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="<PASSWORD123>",
        )

    def test_user_is_not_authenticated(self):
        url = reverse("catalog:collections-create")
        data = {
            "name": "Gold",
        }
        response = self.client.post(url, data=data)
        self.assertNotEqual(response.status_code, 200)
        self.assertFalse(Collection.objects.filter(name=data["name"]).exists())

    def test_user_is_authenticated(self):
        self.client.force_login(self.user)
        url = reverse("catalog:collections-create")
        data = {
            "name": "Gold",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse_lazy("catalog:collections")
        )
        self.assertTrue(Collection.objects.filter(name=data["name"]).exists())

class CollectionUpdateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="<PASSWORD123>",
        )
        self.collection = Collection.objects.create(name="gold", description="some text")

    def test_user_is_not_authenticated(self):
        url = reverse("catalog:collections-update", kwargs={"pk": self.collection.pk})
        data = {"description": "test description",}
        response = self.client.post(url, data=data)
        self.assertNotEqual(response.status_code, 200)
        self.assertFalse(Collection.objects.filter(description=data["description"]).exists())

    def test_user_is_authenticated(self):
        self.client.force_login(self.user)
        url = reverse("catalog:collections-update", kwargs={"pk": self.collection.pk})
        data = {"description": "test description",}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        ###################################################################
        self.assertRedirects(
            response,
            reverse_lazy("catalog:collections")
        )
        #####################################################################
        self.assertTrue(Collection.objects.filter(description=data["description"]).exists())

class CollectionDeleteView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="<PASSWORD123>",
        )
        self.collection = Collection.objects.create(name="gold", description="some text")

    def test_user_is_not_authenticated(self):
        url = reverse("catalog:collections-delete", kwargs={"pk": self.collection.pk})
        response = self.client.post(url)
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(Collection.objects.filter(pk=self.collection.pk).exists())

    def test_user_is_authenticated(self):
        self.client.force_login(self.user)
        url = reverse("catalog:collections-delete", kwargs={"pk": self.collection.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse_lazy("catalog:collections")
        )
        self.assertFalse(Collection.objects.filter(pk=self.collection.pk).exists())
