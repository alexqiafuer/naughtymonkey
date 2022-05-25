from django.urls import path

from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('', getRoutes),
    path('projects/', getProjects),
    path('projects/<str:pk>', getProjects),
    path('projects/<str:pk>/vote/', projectVote),

    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('remove-tag/', removeTag)
]
