
from django.db import models
from django.contrib.auth.models import AbstractUser

class Employee(AbstractUser):
    class Meta:
        verbose_name = "employee"
        verbose_name_plural = "employees"

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    published_date = models.DateField()
    is_borrowed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower_name = models.CharField(max_length=200)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.borrower_name}"
