from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
import time


class AccountsFunctionalTests(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install())
        )

    def tearDown(self):
        self.browser.close()

    def test_signup(self):
        # user navigates to the signup page
        self.browser.get(self.live_server_url + reverse("signup_account"))

        # user fills the sign up form for the first time
        username_input = self.browser.find_element(By.ID, "id_username")
        password1_input = self.browser.find_element(By.ID, "id_password1")
        password2_input = self.browser.find_element(By.ID, "id_password2")

        username_input.send_keys("testuser")
        password1_input.send_keys("password123456")
        password2_input.send_keys("password123456")

        # user submit the form for the first time
        password2_input.send_keys(Keys.RETURN)

        # wait for 2 seconds
        time.sleep(2)

        # after form submit user redirect to  home page
        self.assertEqual(
            self.browser.current_url, self.live_server_url + reverse("home_page")
        )

    def test_login(self):
        # first user need to be created at 'signup_accont'
        self.client.post(
            reverse("signup_account"),
            {
                "username": "testuser",
                "password1": "p@ssword123",
                "password2": "p@ssword123",
            },
        )

        # user navigates to the signup page
        self.browser.get(self.live_server_url + reverse("login_account"))

        # user fills the sign up after 'signup_account'
        username_input = self.browser.find_element(By.ID, "id_username")
        password_input = self.browser.find_element(By.ID, "id_password")

        username_input.send_keys("testuser")
        password_input.send_keys("p@ssword123")

        # user submit the form for the first time
        password_input.send_keys(Keys.RETURN)

        # wait for 2 seconds
        time.sleep(2)

        # after form submit user redirect to  home page
        self.assertEqual(
            self.browser.current_url, self.live_server_url + reverse("home_page")
        )

    def test_logout(self):
        # first user need to be created at 'signup_accont'
        self.client.post(
            reverse("signup_account"),
            {
                "username": "testuser",
                "password1": "p@ssword123",
                "password2": "p@ssword123",
            },
        )

        # second, user need to 'login_account'
        self.client.login(username="testuser", password="p@ssword123")

        # user navigates to the logout page
        self.browser.get(self.live_server_url + reverse("logout_account"))

        # wait for 2 seconds
        time.sleep(2)

        # after form submit user redirect to  home page
        self.assertEqual(
            self.browser.current_url, self.live_server_url + reverse("home_page")
        )
