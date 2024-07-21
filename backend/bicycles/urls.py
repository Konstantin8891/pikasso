from bicycles.views import BicycleCreateListView, RentHistoryView, RentView
from django.urls import path

urlpatterns = [
    path("", BicycleCreateListView.as_view(), name="bicycle_create_list"),
    path("rent/", RentView.as_view(), name="rent_bicycle"),
    path("rent/history/", RentHistoryView.as_view(), name="rent_history"),
]
