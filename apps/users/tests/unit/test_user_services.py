import pytest

from apps.users.models import User
from apps.users.services import AuthService


@pytest.mark.django_db
def test_generate_user_tokens(create_test_user):
    user = User.objects.get(email="test@email.com")
    tokens = AuthService.generate_tokens_for_user(user)
    assert len(tokens) == 2
