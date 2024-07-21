import pytest
from authentication.services import register_user


@pytest.mark.django_db
def test_register_user(guest_client, test_user):
    data = {"email": "test3@example.com", "name": "Test user 3", "password": "Adminqwe1."}
    user = register_user(data=data)
    assert user.name == "Test user 3"
    assert user.check_password("Adminqwe1.") is True
