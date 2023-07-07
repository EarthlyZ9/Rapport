import pytest

from apps.customers.models import Customer
from apps.users.tests.conftest import *

from tests import test_objects


@pytest.fixture(autouse=False, scope="function")
def create_test_customers(db):
    Customer.objects.create(fc_id=1, **test_objects.test_customer_1)
    Customer.objects.create(fc_id=1, **test_objects.test_customer_2)
