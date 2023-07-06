import pytest
from django.test import Client

from apps.products.models import ProductProvider
from apps.users.models import User
from config.test_client_request import ClientRequest


class TestAuthView(object):
    def setup_class(cls):
        cls.request = ClientRequest(Client())
        cls.base_url = "/api/auth"

    def test_login(self, create_test_user):
        url = self.base_url + "/login"
        res = self.request(
            "post", url, {"email": "test@email.com", "password": "test123456"}
        )
        data = res.json()

        assert res.status_code == 200
        assert data["access"]
        assert data["refresh"]
        assert data["email"] == "test@email.com"

    @pytest.mark.django_db
    def test_check_duplicate_email_success(self):
        url = self.base_url + "/check-email"
        res = self.request("post", url, {"email": "test@email.com"})
        self.request.clear_cookies()

        data = res.json()

        assert res.status_code == 200
        assert data["email"] == "test@email.com"

    @pytest.mark.django_db
    def test_check_duplicate_email_failed(self, create_test_user):
        url = self.base_url + "/check-email"
        res = self.request("post", url, {"email": "test@email.com"})
        self.request.clear_cookies()

        assert res.status_code == 409

    @pytest.mark.django_db
    def test_signup_success(self):
        url = self.base_url + "/signup"
        res = self.request(
            "post",
            url,
            {
                "email": "test@email.com",
                "password": "test123456",
                "confirm_password": "test123456",
                "name": "test",
                "affiliation": ProductProvider.KBINS.value,
            },
            {"check-duplicate": "complete"},
        )
        data = res.json()

        created_user = User.objects.get(email="test@email.com")

        assert res.status_code == 201
        assert created_user and created_user.email == "test@email.com"

    @pytest.mark.django_db
    def test_signup_password_mismatch(self):
        url = self.base_url + "/signup"
        res = self.request(
            "post",
            url,
            {
                "email": "test@email.com",
                "password": "test123456",
                "confirm_password": "test123",
                "name": "test",
                "affiliation": ProductProvider.KBINS.value,
            },
            {"check-duplicate": "complete"},
        )

        assert res.status_code == 400

    @pytest.mark.django_db
    def test_signup_duplicate_check_incomplete(self):
        url = self.base_url + "/signup"
        self.request.clear_cookies()
        res = self.request(
            "post",
            url,
            {
                "email": "test@email.com",
                "password": "test123456",
                "confirm_password": "test123456",
                "name": "test",
                "affiliation": ProductProvider.KBINS.value,
            },
        )

        assert res.status_code == 422
