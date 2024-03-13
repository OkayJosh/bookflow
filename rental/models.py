import uuid

from django.db import models
from django_extensions.db.models import TimeStampedModel

from student.models import Student


class Book(TimeStampedModel, models.Model):
    """
    Represents a book in the system.

    Attributes:
        book_id (UUIDField): Unique identifier for the book.
        title (CharField): Title of the book.
        author (CharField): Author of the book.
        page_count (PositiveIntegerField): Number of pages in the book.
        isbn (CharField): ISBN (International Standard Book Number) of the book.
        available_copies (PositiveIntegerField): Number of available copies of the book.

    Methods:
        __str__: Returns a human-readable representation of the book.

    Meta:
        db_table (str): Specifies the database table name for the model.
        verbose_name (str): Human-readable name for a single instance of the model.
        verbose_name_plural (str): Human-readable name for the model in plural form.
    """

    book_id = models.UUIDField(primary_key=True,
                               default=uuid.uuid4,
                               editable=False)
    title = models.CharField(max_length=255,
                             blank=True,
                             null=True)
    author = models.CharField(max_length=255,
                              blank=True,
                              null=True)
    page_count = models.PositiveIntegerField(blank=True,
                                             null=True)
    isbn = models.CharField(max_length=13,
                            blank=True,
                            null=True)

    def __str__(self):
        """
        Returns a human-readable representation of the book.
        If the title is not available, the representation includes the book_id.

        Returns:
            str: Human-readable representation of the book.
        """
        return self.title or f"Book {self.book_id}"

    class Meta:
        db_table = "Book"
        verbose_name = "Book"
        verbose_name_plural = "Books"


class Rental(TimeStampedModel, models.Model):
    """
    Represents a rental transaction in the system.

    Attributes:
        rental_id (UUIDField): Unique identifier for the rental.
        student_id (ForeignKey): Foreign key to the associated student.
        book_id (ForeignKey): Foreign key to the associated book.
        return_date (DateTimeField): Date and time when the book is returned.

    Meta:
        db_table (str): Specifies the database table name for the model.
        verbose_name (str): Human-readable name for a single instance of the model.
        verbose_name_plural (str): Human-readable name for the model in plural form.
    """
    rental_id = models.UUIDField(primary_key=True,
                                 default=uuid.uuid4,
                                 editable=False)
    student_id = models.ForeignKey(Student,
                                   on_delete=models.SET_NULL,
                                   blank=True,
                                   null=True,
                                   related_name='rental_student')
    book_id = models.ForeignKey('Book',
                                on_delete=models.SET_NULL,
                                blank=True,
                                null=True,
                                related_name='rental_book')
    return_date = models.DateTimeField(blank=True,
                                       null=True)
    fee_amount = models.DecimalField(decimal_places=2,
                                     max_digits=200,
                                     blank=True,
                                     null=True)

    class Meta:
        db_table = "Rental"
        verbose_name = "Rental"
        verbose_name_plural = "Rentals"
