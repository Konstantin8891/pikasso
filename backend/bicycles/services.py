from bicycles.models import Bicycle, BicycleUser
from users.tasks import add_bill


def create_bicycle(data):
    return Bicycle.objects.create(**data)


def start_rent(bicycle, user):
    BicycleUser.objects.create(bicycle=bicycle, user=user)


def finish_rent(bicycle, user):
    bicycle_user = BicycleUser.objects.get(bicycle=bicycle, user=user)
    start_rent = bicycle_user.rent_start
    bicycle_user.delete()
    add_bill.delay(bicycle.id, user.id, start_rent)
