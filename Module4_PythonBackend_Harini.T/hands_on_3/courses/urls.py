from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CourseListView,
    CourseDetailView,
    CourseViewSet,
    StudentViewSet,
    EnrollmentViewSet
)

router = DefaultRouter()

router.register(
    'courses-viewset',
    CourseViewSet
)

router.register(
    'students',
    StudentViewSet
)

router.register(
    'enrollments',
    EnrollmentViewSet
)

urlpatterns = [

    # TASK 1
    path(
        'courses/',
        CourseListView.as_view()
    ),

    path(
        'courses/<int:pk>/',
        CourseDetailView.as_view()
    ),

    # TASK 2
    path(
        '',
        include(router.urls)
    ),
]