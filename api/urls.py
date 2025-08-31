from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConfigViewSet

router = DefaultRouter()
router.register(r'configs', ConfigViewSet)

urlpatterns = [
    path('', include(router.urls)),
]