from django.test import SimpleTestCase
from django.urls import resolve, reverse
from accounts import views


class URLTestCase(SimpleTestCase):

    def test_signup_url_resolves(self):
        url = reverse("signup_account")
        self.assertEqual(resolve(url).func, views.signup_account)

    def test_login_url_resolves(self):
        url = reverse("login_account")
        self.assertEqual(resolve(url).func, views.login_account)

    def test_logout_url_resolves(self):
        url = reverse("logout_account")
        self.assertEqual(resolve(url).func, views.logout_account)
