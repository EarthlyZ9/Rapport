import pytest
from django.test import Client

from apps.users.models import User
from apps.users.services import AuthService
from config.test_client_request import ClientRequest
from tests import test_objects


class TestCustomerView(object):
    def setup_class(cls):
        cls.request = ClientRequest(Client())
        cls.base_url = "/api/customers"

    @staticmethod
    def create_token_for_test_user(user: User):
        return AuthService.generate_tokens_for_user(user)["access"]

    @pytest.mark.django_db
    def test_get_all_customers(self, create_test_user, create_test_customers):
        res = self.request(
            "get",
            self.base_url,
            headers={
                "authorization": "Bearer "
                + self.create_token_for_test_user(User.objects.get(id=1))
            },
        )
        data = res.json()

        assert res.status_code == 200
        assert len(data) == 2

    @pytest.mark.django_db
    def test_create_new_customer(self, create_test_user):
        res = self.request(
            "post",
            self.base_url,
            test_objects.test_customer_1,
            headers={
                "authorization": "Bearer "
                + self.create_token_for_test_user((User.objects.get(id=1)))
            },
        )

        data = res.json()

        assert res.status_code == 201
        assert data["name"] == test_objects.test_customer_1["name"]

    @pytest.mark.django_db
    def test_get_customer_by_id(self, create_test_user, create_test_customers):
        url = self.base_url + "/1"
        res = self.request(
            "get",
            url,
            headers={
                "authorization": "Bearer "
                + self.create_token_for_test_user((User.objects.get(id=1)))
            },
        )
        data = res.json()

        assert res.status_code == 200
        assert data["name"] == test_objects.test_customer_1["name"]
        assert type(data["insurances"]) == list

    @pytest.mark.django_db
    def test_get_none_existent_customer_(self, create_test_user):
        url = self.base_url + "/999"
        res = self.request(
            "get",
            url,
            headers={
                "authorization": "Bearer "
                + self.create_token_for_test_user((User.objects.get(id=1)))
            },
        )

        assert res.status_code == 404

    @pytest.mark.django_db
    def test_update_customer_by_id(self, create_test_user, create_test_customers):
        url = self.base_url + "/1"
        res = self.request(
            "patch",
            url,
            {"name": "new name", "enrollment_date": "2023-07-07"},
            headers={
                "authorization": "Bearer "
                + self.create_token_for_test_user(User.objects.get(id=1))
            },
        )
        data = res.json()

        assert res.status_code == 200
        assert data["name"] == "new name"
        assert data["enrollment_date"] == "2023-07-07"

    @pytest.mark.django_db
    def test_update_customer_with_no_permission(
        self, create_test_user, create_test_customers
    ):
        url = self.base_url + "/1"
        res = self.request(
            "patch",
            url,
            {"name": "new name", "enrollment_date": "2023-07-07"},
            headers={
                "authorization": "Bearer "
                + self.create_token_for_test_user(User.objects.get(id=2))
            },
        )
        data = res.json()

        assert res.status_code == 403
