from django.test import TestCase
from accounts.forms import UserCreateForm


class UserCreateFromTestCase(TestCase):

    def test_form_valid_data(self):
        form_data = {
            "username": "testuser",
            "password1": "password23423",
            "password2": "password23423",
        }
        form = UserCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form_data = {
            "username": "testuser",
            "password1": "password23423",
            "password2": "anotherpassw0",
        }
        form = UserCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
