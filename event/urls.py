
from django.urls import *
from .views import *

urlpatterns = [
    path('org/create-event/',addEvent),
    path('get-event-list/',getEventList),
    path('add-rating/',addRating),
    path('get-event/',getEvent),
    path('get-event-list-org/',getEventListOrg),
    path('register-for-event/',registerForEvent),
    path('get-register-data/',getRegisterData),
]