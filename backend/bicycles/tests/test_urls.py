import pytest


@pytest.mark.django_db
def test_list_bicyles(guest_client):
    response = guest_client.get("/api/v1/bicycle/")
    response = response.json()
    assert ("count" in response.keys()) is True
    assert response.get("count") == 1
    assert ("next" in response.keys()) is True
    assert ("previous" in response.keys()) is True
    assert ("results" in response.keys()) is True
    assert len(response["results"]) == 1


@pytest.mark.django_db
def test_create_existing_bicycle(guest_client):
    response = guest_client.post("/api/v1/bicycle/", data={"name": "Bicycle 2", "cost_per_minute": 10})
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_no_cost_bicycle(guest_client):
    response = guest_client.post("/api/v1/bicycle/", data={"name": "Bicycle 3"})
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_no_bicycle(guest_client):
    response = guest_client.post("/api/v1/bicycle/", data={"cost_per_minute": 10})
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_ok(guest_client):
    response = guest_client.post("/api/v1/bicycle/", data={"name": "Bicycle 3", "cost_per_minute": 10})
    assert response.status_code == 201
    response = response.json()
    assert response["id"] == 3
    assert response["name"] == "Bicycle 3"
    assert response["cost_per_minute"] == 10


@pytest.mark.django_db
def test_rent_rented_bike(user_client):
    response = user_client.post("/api/v1/bicycle/rent/", data={"rent": True, "bicycle": 2})
    assert response.status_code == 400


@pytest.mark.django_db
def test_rent_bike_no_bike(user_client):
    response = user_client.post("/api/v1/bicycle/rent/", data={"rent": True})
    assert response.status_code == 400


@pytest.mark.django_db
def test_rent_no_flag(user_client):
    response = user_client.post("/api/v1/bicycle/rent/", data={"bicycle": 1})
    assert response.status_code == 400


@pytest.mark.django_db
def test_rent_bike(user_client):
    response = user_client.post("/api/v1/bicycle/rent/", data={"rent": True, "bicycle": 1})
    assert response.status_code == 200
