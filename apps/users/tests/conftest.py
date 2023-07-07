import pytest
from apps.products.models import ProductProvider
from apps.users.models import User
from tests import test_objects


@pytest.fixture(autouse=False, scope="function")
def create_test_user(db):
    User.objects.create_user(**test_objects.test_user1)
    User.objects.create_user(**test_objects.test_user2)
