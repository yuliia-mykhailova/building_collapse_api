from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *


urlpatterns = [
    path('users/register/', RegisterAPIView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/logout/', LogoutAPIView.as_view(), name='logout'),
    path('users/me/', ProfileAPIView.as_view(), name='profile'),
]
router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='user')
router.register('constructions', ConstructionViewSet, basename='construction')
router.register('foundations', FoundationViewSet, basename='foundation')
router.register('roofs', RoofViewSet, basename='roof')
router.register('walls', WallsViewSet, basename='wall')
router.register('floors', FloorViewSet, basename='floor')
router.register('measurements', MeasurementViewSet, basename='measurement')
router.register('evaluations', EvaluationViewSet, basename='evaluation')
router.register('predictions', PredictionViewSet, basename='prediction')
urlpatterns += router.urls
