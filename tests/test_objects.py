from apps.customers.models import Customer
from apps.products.models import ProductProvider

test_user1 = dict(
    id=1,
    email="test@email.com",
    password="test123456",
    affiliation=ProductProvider.KBINS.value,
)

test_user2 = dict(
    id=2,
    email="test2@email.com",
    password="test123456",
    affiliation=ProductProvider.KBINS.value,
)

test_customer_1 = dict(
    id=1,
    name="customer1",
    date_of_birth="2000-07-29",
    calendar=Customer.Calendar.SOLAR.value,
)

test_customer_2 = dict(
    id=2,
    name="customer2",
    date_of_birth="2003-08-01",
    calendar=Customer.Calendar.SOLAR.value,
)
