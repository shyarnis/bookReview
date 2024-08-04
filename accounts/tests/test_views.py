from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import UserCreateForm


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse("signup_account")
        self.login_url = reverse("login_account")
        self.logout_url = reverse("logout_account")
        self.home_url = reverse("home_page")

        # Create a test user.
        self.test_user = User.objects.create_user(
            username="testuser", password="testpassword123"
        )

    def test_signup_account_GET(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup.html")
        self.assertIsInstance(response.context["form"], UserCreateForm)

    def test_signup_account_POST_success(self):
        data = {
            "username": "newuser",
            "password1": "newpassword123",
            "password2": "newpassword123",
        }
        response = self.client.post(self.signup_url, data)
        self.assertRedirects(response, self.home_url)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_signup_account_POST_password_mismatch(self):
        data = {
            "username": "newuser",
            "password1": "password123",
            "password2": "password456",
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup.html")
        self.assertContains(response, "Passwords do not match")

    def test_signup_account_POST_username_taken(self):
        data = {
            "username": "testuser",  # This username already exists
            "password1": "password123",
            "password2": "password123",
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup.html")
        self.assertContains(response, "Username already taken")

    def test_login_account_GET(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        self.assertIsInstance(response.context["form"], AuthenticationForm)

    def test_login_account_POST_success(self):
        data = {"username": "testuser", "password": "testpassword123"}
        response = self.client.post(self.login_url, data)
        self.assertRedirects(response, self.home_url)

    def test_login_account_POST_invalid_credentials(self):
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        self.assertContains(response, "username and password do not match")

    def test_logout_account(self):
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.home_url)

        # Check that the user is logged out
        response = self.client.get(self.home_url)
        self.assertFalse(response.context["user"].is_authenticated)
