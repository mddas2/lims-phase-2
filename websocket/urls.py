from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('notification', views.NotificationViewSet, basename="apis/NotificationViewSet")


urlpatterns = [
    path('', include(router.urls)),
]