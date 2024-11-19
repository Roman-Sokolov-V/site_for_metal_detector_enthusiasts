from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from  django.urls import reverse, reverse_lazy

from catalog.form import UserSerchForm
from catalog.models import Finding


class UserListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="<PASSWORD123>",
        )
        self.another_user = get_user_model().objects.create_user(
            username="another_user",
            password="<anotherPASSWORD1>",
        )
        self.url = reverse("catalog:comrades")

    def test_context_data(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(response.context["search_form"], UserSerchForm)

    def test_get_queryset(self):
        response = self.client.get(f"{self.url}?username=ad")
        self.assertEqual(response.status_code, 200)
        queryset = response.context["user_list"]
        self.assertEqual(list(queryset), list(get_user_model().objects.filter(username__icontains="ad")))


class UserDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="<PASSWORD123>",
        )
        self.another_user = get_user_model().objects.create_user(
            username="another_user",
            password="<anotherPASSWORD1>",
        )
        self.findings = Finding.objects.create(name="test", user=self.user)
        self.another_findings = Finding.objects.create(name="test2", user=self.another_user)


    def test_get_queryset(self):
        url = reverse("catalog:comrades-detail", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["user"].findings.all()), list(Finding.objects.filter(user=self.user)))

class UserCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_is_not_authenticated(self):
        url = reverse("catalog:comrades-create")
        data = {
            "username": "new_user",
            "password1": "<PASSdfgdf123WORD>",
            "password2": "<PASSdfgdf123WORD>",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse_lazy("catalog:comrades")
        )

    def test_user_is_authenticated(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="<PASSWORD123>",
        )
        self.client.force_login(self.user)
        url = reverse("catalog:comrades-create")
        data = {
            "username": "new_user",
            "password1": "<PASSdfgdf123WORD>",
            "password2": "<PASSdfgdf123WORD>",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 403)

class UserUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="<PASSWORD123>",
        )
        self.user = get_user_model().objects.create_user(
            username="user",
            password="<PASSdff12ORD>",
            first_name="first_name",
            last_name="last_name",
            detector_model="detector_model",
        )
        self.another_user = get_user_model().objects.create_user(
            username="another_user",
            password="<PASSdff12dORD>",
        )
    def test_user_is_owner(self):
        self.client.force_login(self.user)
        url = reverse("catalog:comrades-update", kwargs={"pk": self.user.pk})
        data = {
            "first_name": "new_user_first_name",
            "last_name": "new_user_last_name",
            "detector_model": "new_user_detector_model",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse_lazy("catalog:comrades")
        )
        self.assertEqual(
            data,
            get_user_model().objects.values("first_name", "last_name", "detector_model").get(pk=self.user.pk)
        )

    def test_user_is_superuser(self):
        self.client.force_login(self.admin_user)
        url = reverse("catalog:comrades-update", kwargs={"pk": self.user.pk})
        data = {
            "first_name": "new_user_first_name",
            "last_name": "new_user_last_name",
            "detector_model": "new_user_detector_model",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse_lazy("catalog:comrades")
        )
        self.assertEqual(
            data,
            get_user_model().objects.values("first_name", "last_name", "detector_model").get(pk=self.user.pk)
        )

    def test_user_is_not_superuser_is_not_owner(self):
        self.client.force_login(self.another_user)
        url = reverse("catalog:comrades-update", kwargs={"pk": self.user.pk})
        data = {
            "first_name": "new_user_first_name",
            "last_name": "new_user_last_name",
            "detector_model": "new_user_detector_model",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse_lazy("catalog:comrades-detail", kwargs={"pk": self.user.pk})
        )
        self.assertNotEqual(
            data,
            get_user_model().objects.values("first_name", "last_name", "detector_model").get(pk=self.user.pk)
        )

    def test_user_is_not_authenticated(self):
        url = reverse("catalog:comrades-update", kwargs={"pk": self.user.pk})
        data = {
            "first_name": "new_user_first_name",
            "last_name": "new_user_last_name",
            "detector_model": "new_user_detector_model",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse_lazy("login")
        )
        self.assertNotEqual(
            data,
            get_user_model().objects.values("first_name", "last_name", "detector_model").get(pk=self.user.pk)
        )

class UserDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="<PASSWORD123>",
        )
        self.user = get_user_model().objects.create_user(
            username="user",
            password="<PASSdff12ORD>",
            first_name="first_name",
            last_name="last_name",
            detector_model="detector_model",
        )
        self.another_user = get_user_model().objects.create_user(
            username="another_user",
            password="<PASSdff12dORD>",
        )

    def test_user_is_owner(self):
        self.client.force_login(self.user)
        url = reverse("catalog:comrades-delete", kwargs={"pk": self.user.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse_lazy("catalog:comrades")
        )
        self.assertFalse(get_user_model().objects.filter(pk=self.user.pk).exists())

    def test_user_is_superuser(self):
        self.client.force_login(self.admin_user)
        url = reverse("catalog:comrades-delete", kwargs={"pk": self.user.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse_lazy("catalog:comrades")
        )
        self.assertFalse(get_user_model().objects.filter(pk=self.user.pk).exists())

    def test_user_is_not_superuser_is_not_owner(self):
        self.client.force_login(self.another_user)
        url = reverse("catalog:comrades-delete", kwargs={"pk": self.user.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse_lazy("catalog:comrades-detail", kwargs={"pk": self.user.pk})
        )
        self.assertTrue(get_user_model().objects.filter(pk=self.user.pk).exists())

    def test_user_is_not_authenticated(self):
        url = reverse("catalog:comrades-delete", kwargs={"pk": self.user.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse_lazy("login")
        )
        self.assertTrue(get_user_model().objects.filter(pk=self.user.pk).exists())