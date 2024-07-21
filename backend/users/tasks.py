import asyncio

from bicycles.models import Bicycle
from celery import shared_task
from django.utils import timezone
from users.models import UserBill


async def add_bill_task(bicycle_id, user_id, start_rent):
    now = timezone.now()
    rent_range = (now - start_rent).total_seconds()
    rent_range = rent_range // 60
    bicycle = await Bicycle.objects.aget(id=bicycle_id)
    total_cost = bicycle.cost_per_minute * rent_range
    await UserBill.objects.acreate(user_id=user_id, bill=total_cost, duration=rent_range)


@shared_task
def add_bill(bicycle_id, user_id, start_rent):
    asyncio.run(add_bill_task(bicycle_id, user_id, start_rent))
