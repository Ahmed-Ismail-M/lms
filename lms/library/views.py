# library/views.py

from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Book, BorrowRecord
from library.serializers.book_serializers import BookSerializer, BorrowRecordSerializer
from library.serializers.emp_serializers import *
from django.utils.decorators import method_decorator
from library.mw import auth_required, allowed_users
from django.contrib.auth import login

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    @method_decorator(auth_required)
    @method_decorator(allowed_users(["Employee"]))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @method_decorator(auth_required)
    @method_decorator(allowed_users(["Employee"]))
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @method_decorator(auth_required)
    @method_decorator(allowed_users(["Employee"]))
    @action(detail=True, methods=['post'])
    def borrow(self, request, pk=None):
        book = self.get_object()
        if book.is_borrowed:
            return Response({"error": "Book is already borrowed"}, status=status.HTTP_400_BAD_REQUEST)

        borrower_name = request.data.get('borrower_name')
        if not borrower_name:
            return Response({"error": "Borrower name is required"}, status=status.HTTP_400_BAD_REQUEST)

        borrow_record = BorrowRecord.objects.create(book=book, borrower_name=borrower_name)
        book.is_borrowed = True
        book.save()
        return Response(BorrowRecordSerializer(borrow_record).data, status=status.HTTP_201_CREATED)

    @method_decorator(auth_required)
    @method_decorator(allowed_users(["Employee"]))
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        book = self.get_object()
        if not book.is_borrowed:
            return Response({"error": "Book is not borrowed"}, status=status.HTTP_400_BAD_REQUEST)

        borrow_record = BorrowRecord.objects.filter(book=book, return_date__isnull=True).first()
        if not borrow_record:
            return Response({"error": "No active borrow record found for this book"}, status=status.HTTP_400_BAD_REQUEST)

        borrow_record.return_date = request.data.get('return_date')
        borrow_record.save()
        book.is_borrowed = False
        book.save()
        return Response(BorrowRecordSerializer(borrow_record).data, status=status.HTTP_200_OK)


class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer

    def get_queryset(self):
        queryset = BorrowRecord.objects.all()
        borrower_name = self.request.query_params.get('borrower_name', None)
        if borrower_name is not None:
            queryset = queryset.filter(borrower_name=borrower_name)
        return queryset




class RegisterAPI(generics.GenericAPIView):
    serializer_class = EmployeeRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        return Response(
            {"user_id": user.id}, status=status.HTTP_201_CREATED
        )


class LoginAPI(generics.GenericAPIView):
    serializer_class = EmployeeLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = self.serializer_class(
            data=request.data, context={"request": request}
        )

        serializer_class.is_valid(raise_exception=True)
        user = serializer_class.validated_data["user"]
        login(request, user)
        return Response(
            {"user_id": user.id}, status=status.HTTP_200_OK
        )