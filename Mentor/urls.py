from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MentorViewSet, StudentViewSet

router = DefaultRouter()
router.register(r'mentors', MentorViewSet)
router.register(r'students', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
