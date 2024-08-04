from django.test import SimpleTestCase
from django.urls import resolve, reverse
from books import views


class URLTestCase(SimpleTestCase):

    def test_detail_url_resolves(self):
        url = reverse(
            "detail", args=[55]
        )  # 55 is <int:book_id>, it could be any integer.
        self.assertEqual(resolve(url).func, views.detail)

    def test_create_url_resolves(self):
        url = reverse("create_review", args=[1])
        self.assertEqual(resolve(url).func, views.create_review)

    def test_update_url_resolves(self):
        url = reverse("update_review", args=[334])
        self.assertEqual(resolve(url).func, views.update_review)

    def test_delete_url_resolves(self):
        url = reverse("delete_review", args=[3])
        self.assertEqual(resolve(url).func, views.delete_review)
