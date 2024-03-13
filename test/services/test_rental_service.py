from datetime import datetime, timedelta
from unittest.mock import patch

from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.utils import timezone

from rental.models import Book, Rental
from services.book_rental_service import OpenLibraryBookRentalService
from student.models import Student


class OpenLibraryBookRentalServiceTest(TestCase):
    def setUp(self):
        self.service = OpenLibraryBookRentalService()
        hashed_password = make_password('password')
        self.student = Student.objects.create(
                username='test',
                phone_number='12345678',
                address='address',
                email='test@email.com',
                first_name='first_name',
                last_name='last_name',
                password=hashed_password,  # Save the hashed password
                is_staff=True,
                is_active=True
            )

    def test_search_book(self):
        # Mocking the response from OpenLibrary API
        with patch('services.book_rental_service.OpenLibraryBookRentalService.search_book') as mock_get:
            mock_get.return_value = [{
                "docs": [
                    {"title": "Book Title", "author_name": ["Author Name"], "number_of_pages_median": 200}
                ]
            }]
            books = self.service.search_book("Book Title")
            self.assertEqual(len(books), 1)
            self.assertEqual(books[0]['docs'][0]['title'], "Book Title")
            self.assertEqual(books[0]['docs'][0]['author_name'], ["Author Name"])
            self.assertEqual(books[0]['docs'][0]['number_of_pages_median'], 200)

    def test_rent_book(self):
        # Creating a mock book object
        book_title = "Mock Book"
        author_name = "Mock Author"
        page_count = 300
        isbn = "1234567890"
        return_date = timezone.now() + timedelta(days=14)  # Return date after 2 weeks

        # Renting the book
        rental = self.service.rent_book(student_id=self.student.student_id, title=book_title, author=author_name,
                                         page_count=page_count, isbn=isbn, return_date=return_date.strftime('%B %d, %Y, %I:%M %p'))

        # Checking if the rental is saved properly
        self.assertEqual(rental.student_id_id, self.student.student_id)
        self.assertEqual(rental.book_id.title, book_title)
        self.assertEqual(rental.book_id.author, author_name)
        self.assertEqual(rental.book_id.page_count, page_count)
        self.assertEqual(rental.book_id.isbn, isbn)
        # self.assertEqual(rental.return_date.replace(tzinfo=None), return_date.replace(tzinfo=None))

    def test_calculate_rental_cost(self):
        rented_date = timezone.now() - timedelta(days=30)  # Rented 30 days ago
        return_date_within_month = rented_date + timedelta(days=15)  # Return within a month
        return_date_after_month = rented_date + timedelta(days=45)  # Return after a month
        number_of_pages = 200

        # Rental cost when returning within a month (should be 0)
        cost_within_month = self.service.calculate_rental_cost(number_of_pages, rented_date, return_date_within_month)
        self.assertEqual(cost_within_month, 0)

        # Rental cost when returning after a month
        cost_after_month = self.service.calculate_rental_cost(number_of_pages, rented_date, return_date_after_month)
        expected_cost = number_of_pages * OpenLibraryBookRentalService.COST_PER_PAGE
        self.assertEqual(cost_after_month, expected_cost)

    def test_rent_extension(self):
        # Creating a mock rental object
        rental = Rental.objects.create(student_id=self.student, book_id=Book.objects.create(title="Mock Book",
                                                                                  author="Mock Author",
                                                                                  page_count=200,
                                                                                  isbn="1234567890"),
                                       return_date=timezone.now() + timedelta(days=14))

        # Extending the rental return date
        new_return_date = timezone.now() + timedelta(days=28)
        self.service.rent_extension(rental_id=rental.rental_id, return_date=new_return_date.strftime('%Y-%m-%d'))

        # Checking if the return date is updated and fee calculated correctly
        rental.refresh_from_db()
        # self.assertEqual(rental.return_date, new_return_date)
        expected_fee = rental.book_id.page_count * OpenLibraryBookRentalService.COST_PER_PAGE
        expected_fee = self.service.calculate_rental_cost(number_of_pages=rental.book_id.page_count,
                                                          rented_date=rental.created, return_date=rental.return_date)
        self.assertEqual(rental.fee_amount, expected_fee)
