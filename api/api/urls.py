from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from basketball.views import *

router = routers.DefaultRouter()

router.register(r'players', PlayersViewSet, basename="Players")
router.register(r'teams', TeamsViewSet, basename="Teams")
router.register(r'games', GamesViewSet, basename="Games")
router.register(r'user', UserRegistrationViewSet, basename="Users")


urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomAuthToken.as_view(), name='api-token-auth'),
    path('players/<uuid:player_uuid>/', PlayerDetailView.as_view(), name='player_detail')
]