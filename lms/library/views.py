# library/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Book, BorrowRecord
from .serializers import BookSerializer, BorrowRecordSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

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
