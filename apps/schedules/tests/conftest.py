import pytest

from apps.schedules.models import CustomerSchedule
from tests import test_objects
from apps.customers.tests.conftest import *
from apps.users.tests.conftest import *


@pytest.fixture(autouse=False, scope="function")
def create_test_schedules(db):
    CustomerSchedule.objects.create(fc_id=1, **test_objects.test_schedule_1)
    CustomerSchedule.objects.create(fc_id=1, **test_objects.test_schedule_2)
