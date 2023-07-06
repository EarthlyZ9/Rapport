import pytest
from apps.products.models import ProductProvider
from apps.users.models import User


@pytest.fixture(autouse=False, scope="function")
def create_test_user(db):
    User.objects.create_user(
        email="test@email.com",
        password="test123456",
        affiliation=ProductProvider.KBINS.value,
    )
