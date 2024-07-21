import os

import pytest
from bicycles.models import Bicycle, BicycleUser
from django.core.management import call_command
from rest_framework.test import APIClient
from users.models import User


@pytest.fixture(scope="session")
def delete_db():
    try:
        os.remove("db_test.sqlite3")
    except Exception:
        pass


@pytest.fixture(scope="session")
def django_db_setup(delete_db, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("sqlflush")
    with django_db_blocker.unblock():
        call_command("migrate", "--noinput")
    yield


@pytest.fixture(autouse=True, scope="session")
def test_user(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user = User.objects.create(
            name="Test user 1",
            email="test1@example.com",
        )
        user.set_password("Adminqwe1.")
        user.save()


@pytest.fixture(autouse=True, scope="session")
def test_user_with_rented_bicycle(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user = User.objects.create(
            name="Test user 2",
            email="test2@example.com",
        )
        user.set_password("Adminqwe1.")
        user.save()


@pytest.fixture(autouse=True, scope="session")
def test_bicycle_not_rented(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        Bicycle.objects.create(name="Bicycle 1", cost_per_minute=10)


@pytest.fixture(autouse=True, scope="session")
def test_bicycle_rented(django_db_setup, django_db_blocker, test_user_with_rented_bicycle):
    with django_db_blocker.unblock():
        user = User.objects.get(email="test2@example.com")
        bicycle = Bicycle.objects.create(name="Bicycle 2", cost_per_minute=5)
        BicycleUser.objects.create(bicycle=bicycle, user=user)


@pytest.fixture(autouse=True, scope="session")
def guest_client():
    return APIClient()


@pytest.fixture(autouse=True, scope="session")
def user_client(guest_client, django_db_blocker, test_user):
    with django_db_blocker.unblock():
        client = APIClient()
        response = guest_client.post(
            "/api/v1/auth/login/", data={"email": "test1@example.com", "password": "Adminqwe1."}
        )
        token = str(response.json().get("access"))
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        return client
