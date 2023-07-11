import copy

import pytest
from django.test import Client

from apps.schedules.models import CustomerSchedule
from apps.users.models import User
from apps.users.services import AuthService
from config.test_client_request import ClientRequest
from tests import test_objects


class TestCustomerScheduleView(object):
    def setup_class(cls):
        cls.request = ClientRequest(Client())
        cls.base_url = "/api/schedules"

    @staticmethod
    def create_token_for_test_user(user: User):
        return AuthService.generate_tokens_for_user(user)["access"]

    @pytest.mark.django_db
    def test_get_all_schedules(
        self, create_test_user, create_test_customers, create_test_schedules
    ):
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
        assert len(data["items"]) == 2

    @pytest.mark.django_db
    def test_create_new_schedule(self, create_test_user, create_test_customers):
        res = self.request(
            "post",
            self.base_url,
            test_objects.test_schedule_1,
            headers={
                "authorization": "Bearer "
                + self.create_token_for_test_user((User.objects.get(id=1)))
            },
        )

        data = res.json()

        assert res.status_code == 201
        assert data["customer"]["id"] == 1
        assert data["fc"] == 1

    @pytest.mark.django_db
    def test_create_new_schedule_with_invalid_date(
        self, create_test_user, create_test_customers
    ):
        test_schedule = copy.deepcopy(test_objects.test_schedule_1)
        test_schedule["date"] = "2023-07-59"
        res = self.request(
            "post",
            self.base_url,
            test_schedule,
            headers={
                "authorization": "Bearer "
                + self.create_token_for_test_user((User.objects.get(id=1)))
            },
        )

        assert res.status_code == 400

    @pytest.mark.django_db
    def test_get_schedule_by_id(
        self, create_test_user, create_test_customers, create_test_schedules
    ):
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
        assert data["title"] == test_objects.test_schedule_1["title"]
        assert type(data["customer"]) == dict
        assert data["has_end_time"] == False

    @pytest.mark.django_db
    def test_get_none_existent_schedule(self, create_test_user, create_test_customers):
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
    def test_update_schedule_by_id(
        self, create_test_user, create_test_customers, create_test_schedules
    ):
        url = self.base_url + "/1"
        res = self.request(
            "patch",
            url,
            {"customer_id": 2, "end_time": "14:00", "start_time": "13:00"},
            headers={
                "authorization": "Bearer "
                + self.create_token_for_test_user(User.objects.get(id=1))
            },
        )
        data = res.json()

        assert res.status_code == 200
        assert data["customer"]["id"] == 2
        assert data["has_end_time"] == True

    @pytest.mark.django_db
    def test_update_schedule_add_end_time_without_start_time(
        self, create_test_user, create_test_customers, create_test_schedules
    ):
        url = self.base_url + "/1"
        res = self.request(
            "patch",
            url,
            {"end_time": "14:00"},
            headers={
                "authorization": "Bearer "
                + self.create_token_for_test_user(User.objects.get(id=1))
            },
        )

        assert res.status_code == 400

    @pytest.mark.django_db
    def test_update_schedule_invalid_time_format(
        self, create_test_user, create_test_customers, create_test_schedules
    ):
        url = self.base_url + "/1"
        res = self.request(
            "patch",
            url,
            {"start_time": "24:59"},
            headers={
                "authorization": "Bearer "
                + self.create_token_for_test_user(User.objects.get(id=1))
            },
        )

        assert res.status_code == 400

    @pytest.mark.django_db
    def test_update_schedule_with_no_permission(
        self, create_test_user, create_test_customers, create_test_schedules
    ):
        url = self.base_url + "/1"
        res = self.request(
            "patch",
            url,
            {"customer_id": 2, "end_time": "14:00", "start_time": "13:00"},
            headers={
                "authorization": "Bearer "
                + self.create_token_for_test_user(User.objects.get(id=2))
            },
        )

        assert res.status_code == 403

    @pytest.mark.django_db
    def test_delete_schedule_by_id(
        self, create_test_user, create_test_customers, create_test_schedules
    ):
        url = self.base_url + "/1"
        res = self.request(
            "del",
            url,
            headers={
                "authorization": "Bearer "
                + self.create_token_for_test_user(User.objects.get(id=1))
            },
        )

        schedules_count = CustomerSchedule.objects.all().count()

        assert res.status_code == 204
        assert schedules_count == 1

    @pytest.mark.django_db
    def test_delete_schedule_with_no_permission(
        self, create_test_user, create_test_customers, create_test_schedules
    ):
        url = self.base_url + "/1"
        res = self.request(
            "del",
            url,
            headers={
                "authorization": "Bearer "
                + self.create_token_for_test_user(User.objects.get(id=2))
            },
        )

        assert res.status_code == 403

    @pytest.mark.django_db
    def test_cascade_schedules_on_customer_deletion(
        self, create_test_user, create_test_customers, create_test_schedules
    ):
        url = "/api/schedules/1"
        res = self.request(
            "del",
            url,
            headers={
                "authorization": "Bearer "
                + self.create_token_for_test_user(User.objects.get(id=1))
            },
        )

        schedules_count = CustomerSchedule.objects.filter(customer_id=1).count()

        assert res.status_code == 204
        assert schedules_count == 0
