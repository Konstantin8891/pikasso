import pytest
from bicycles.models import Bicycle, BicycleUser
from bicycles.services import create_bicycle, finish_rent, start_rent
from django.test.utils import override_settings
from users.models import User


@pytest.mark.django_db
def test_create_bicycle():
    bicycle = create_bicycle(data={"name": "Bicycle 3", "cost_per_minute": 5})
    assert bicycle.name == "Bicycle 3"
    assert bicycle.cost_per_minute == 5


@pytest.mark.django_db
def test_start_rent():
    user = User.objects.get(email="test1@example.com")
    bicycle = Bicycle.objects.get(name="Bicycle 1")
    start_rent(user=user, bicycle=bicycle)
    assert BicycleUser.objects.filter(bicycle=bicycle, user=user).exists() is True


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@override_settings(
    CELERY_TASK_EAGER_PROPAGATES=True,
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_BROKER_URL="memory://",
    CELERY_RESULT_BACKEND="cache+memory://",
)
def test_finish_rent():
    user = User.objects.get(email="test2@example.com")
    bicycle = Bicycle.objects.get(name="Bicycle 2")
    finish_rent(bicycle, user)
    assert BicycleUser.objects.filter(bicycle=bicycle, user=user).exists() is False
