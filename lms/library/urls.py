# library/urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BorrowRecordViewSet, RegisterAPI, LoginAPI

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'borrow-records', BorrowRecordViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path("api/v1/register", RegisterAPI.as_view(), name="register"),
    path("api/v1/login", LoginAPI.as_view(), name="login"),
]
