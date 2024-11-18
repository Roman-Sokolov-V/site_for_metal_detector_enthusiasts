from django.test import TestCase
from catalog.models import User, Finding, Collection, Image


class ModelsTests(TestCase):
    def test_user_str(self):
        user = User.objects.create_user(username="test", password="<PASSWORD>")
        self.assertEqual(str(user), "test")

    def test_finding_str(self):
        user = User.objects.create_user(username="test", password="<PASSWORD>")
        finding = Finding.objects.create(name="test", user=user)
        self.assertEqual(finding.name, "test")

    def test_collection_str(self):
        collection = Collection.objects.create(name="test")
        self.assertEqual(str(collection), "test")

    def test_image_str(self):
        user = User.objects.create_user(username="test", password="<PASSWORD>")
        finding = Finding.objects.create(name="test", user=user)
        image = Image.objects.create(finding=finding)
        self.assertEqual(str(image), f"image {finding.name} id: {image.pk}")