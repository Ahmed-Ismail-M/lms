# library/urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BorrowRecordViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'borrow-records', BorrowRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
