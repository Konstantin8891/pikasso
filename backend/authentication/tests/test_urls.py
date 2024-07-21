import pytest
from rest_framework_simplejwt.tokens import BlacklistedToken, OutstandingToken


@pytest.mark.django_db
def test_logout(user_client, guest_client):
    response = guest_client.post("/api/v1/auth/login/", data={"email": "test1@example.com", "password": "Adminqwe1."})
    response = response.json()
    refresh = response.get("refresh")
    response = user_client.post("/api/v1/auth/logout/", data={"refresh": refresh})
    assert response.status_code == 200
    outstanding_token = OutstandingToken.objects.filter(token=refresh)
    assert outstanding_token.exists() is True
    assert BlacklistedToken.objects.filter(token=outstanding_token.first()).exists() is True


@pytest.mark.django_db
def test_register_no_email(guest_client):
    response = guest_client.post("/api/v1/auth/register/", data={"password": "Adminqwe1.", "name": "Test user 2"})
    assert response.status_code == 400


@pytest.mark.django_db
def test_register_no_password(guest_client):
    response = guest_client.post("/api/v1/auth/register/", data={"email": "test4@example.com", "name": "Test user 2"})
    assert response.status_code == 400


@pytest.mark.django_db
def test_register_no_name(guest_client):
    response = guest_client.post(
        "/api/v1/auth/register/", data={"email": "test4@example.com", "password": "Adminqwe1."}
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_register_ok(guest_client):
    response = guest_client.post(
        "/api/v1/auth/register/", data={"email": "test4@example.com", "password": "Adminqwe1.", "name": "Test user 4"}
    )
    assert response.status_code == 201
    response = response.json()
    assert response.get("email") == "test4@example.com"
    assert response.get("name") == "Test user 4"
