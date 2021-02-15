from django.test.testcases import SimpleTestCase, TestCase
from django.urls import resolve, reverse

from login import views
from login.models import OpenIDCUser, DiscordUser
# Create your tests here.

class TestUrls(SimpleTestCase):

    def test_url_openidc(self):
        url = reverse('OpenID-Connect-response')
        self.assertEquals(resolve(url).func, views.openidc_response)

    def test_url_discord_oauth(self):
        url = reverse('Discord-login')
        self.assertEquals(resolve(url).func, views.discord_oauth2)

    def test_url_discord_redirect(self):
        url = reverse('Discord-response')
        self.assertEquals(resolve(url).func, views.discord_oauth2_redirect)

    def test_url_logged_in(self):
        url = reverse('logged-in')
        self.assertEquals(resolve(url).func, views.get_authenticated_user)

class TestModels(TestCase):

    def test_model_openidc_user(self):
        self.openidc_user1 = OpenIDCUser.objects.create(
            username="abc123",
            name="Bob Ross",
            email="abc123@aber.ac.uk",
            usertype="undergrad"
        )
        self.assertEquals(self.openidc_user1.username, "abc123")
        self.assertEquals(self.openidc_user1.name, "Bob Ross")
        self.assertEquals(self.openidc_user1.email, "abc123@aber.ac.uk")
        self.assertEquals(self.openidc_user1.usertype, "undergrad")

    def test_model_discord_user(self):
        self.discord_user1 = DiscordUser.objects.create(
            id=12213123123,
            username="Bob Ross",
            openidc=self.discord_user1
        )
        self.assertEquals(self.discord_user1.id, 12213123123)
        self.assertEquals(self.discord_user1.username, "Bob Ross")
        self.assertEquals(self.discord_user1.openidc, self.openidc_user1)