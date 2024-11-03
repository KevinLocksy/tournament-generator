from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class SignUpTests(TestCase):
    """Test class to test the signup feature"""

    def test_signup_page_accessible(self):
        """Test if signup page is accessible"""
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)

    def test_signup_successful(self):
        """Test if signup page is accessible"""
        response = self.client.post(
            reverse("signup"),
            {
                "username": "user",
                "password1": "TestPassword123",
                "password2": "TestPassword123",
            },
        )
        self.assertEqual(response.status_code, 302)  # redirects after signup
        self.assertTrue(
            User.objects.filter(username="user").exists()
        )  # Check if user has been created
        self.assertRedirects(response, reverse("home"))  # redirects to home page

    def test_signup_failed_due_to_criteria(self):
        """Test if signup page fails due to password not meeting criteria"""
        response = self.client.post(
            reverse("signup"),
            {"username": "user", "password1": "user", "password2": "user"},
        )
        self.assertEqual(response.status_code, 200)

    def test_signup_failed_due_to_mismatch(self):
        """Test if signup page fails due to mismatched passwords"""
        response = self.client.post(
            reverse("signup"),
            {"username": "user", "password1": "TestPassword123", "password2": "user"},
        )
        self.assertEqual(response.status_code, 200)


class LoginTests(TestCase):
    """Test class to test the login feature"""

    def setUp(self):
        self.testuser = get_user_model().objects.create_user(
            username="user",
            password="user",
        )

    def test_login_page_accessible(self):
        """Test if login page is accessible"""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_login_successful(self):
        """Test login from page with right credentials"""
        response = self.client.post(
            reverse("login"), {"username": "user", "password": "user"}
        )
        self.assertEqual(response.status_code, 302)  # redirects to home page
        self.assertRedirects(response, reverse("home"))  # redirects to home page

    def test_login_page_fail(self):
        """Test login from page with wrong credentials"""
        response = self.client.post(
            reverse("login"), {"username": "user", "password": "pazokeapzo"}
        )
        self.assertEqual(response.status_code, 200)  # stays on same page


class LogoutTests(TestCase):
    """Test class to test the logout feature"""

    def setUp(self):
        self.testuser = get_user_model().objects.create_user(
            username="user",
            password="TestPassword123",
        )
        self.client.login(username="TestPassword123", password="TestPassword123")

    def test_logout(self):
        """Test that a user is redirected to the home page after logging out"""
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)  # redirects after logout
        self.assertRedirects(response, reverse("home"))
