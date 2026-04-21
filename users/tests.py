from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthFlowTests(TestCase):
    def test_home_redirects_anonymous_to_login(self) -> None:
        response = self.client.get(reverse("home"), follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.url)

    def test_register_logs_in_and_redirects_home(self) -> None:
        password = "xK9#mP2$vL8@nQ4!"
        response = self.client.post(
            reverse("users:register"),
            {
                "username": "alice",
                "email": "alice@example.com",
                "password1": password,
                "password2": password,
            },
        )
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(User.objects.filter(username="alice").exists())
        user = User.objects.get(username="alice")
        self.assertEqual(user.email, "alice@example.com")
        home = self.client.get(reverse("home"))
        self.assertEqual(home.status_code, 200)
        self.assertContains(home, "alice")

    def test_logout_post(self) -> None:
        User.objects.create_user("bob", "bob@example.com", "yR3!nT6%wH1@bF9#")
        self.client.login(username="bob", password="yR3!nT6%wH1@bF9#")
        out = self.client.post(reverse("users:logout"))
        self.assertEqual(out.status_code, 302)
        self.assertIn(reverse("users:login"), out.url)
