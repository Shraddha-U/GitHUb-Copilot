
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .views import UserViewSet, TeamViewSet, WorkoutViewSet, ActivityViewSet, LeaderboardViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'workouts', WorkoutViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'leaderboard', LeaderboardViewSet)

import os
@api_view(['GET'])
def api_root(request, format=None):
    codespace_name = os.environ.get('CODESPACE_NAME')
    if codespace_name:
        base_url = f"https://{codespace_name}-8000.app.github.dev/api/"
    else:
        # fallback to request host (localhost or other)
        base_url = request.build_absolute_uri('/')
        if not base_url.endswith('/'):
            base_url += '/'
    return Response({
        'users': base_url + 'users/',
        'teams': base_url + 'teams/',
        'workouts': base_url + 'workouts/',
        'activities': base_url + 'activities/',
        'leaderboard': base_url + 'leaderboard/',
    })

from django.urls import re_path
urlpatterns = [
    path('api/', api_root, name='api_root'),
    path('api/', include(router.urls)),
]
