import calendar
import datetime
from datetime import timedelta

import pytz
import requests
from django.http import HttpResponse
import logging

from rental.models import Book, Rental

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenLibraryBookRentalService:
    """
    A class for initiating book rentals using the OpenLibrary API.

    Attributes:
        api_base_url (str): The base URL for OpenLibrary API.

    Methods:
        initiate_new_rental: Initiates a new book rental by fetching book details from OpenLibrary.
        calculate_rental_cost: Calculates the rental cost based on the number of pages.
        save_rental_details: Saves rental details in the system or database.

    Example Usage:
        open_library_rental = OpenLibraryBookRental()
        open_library_rental.initiate_new_rental("The Catcher in the Rye")
    """
    OPEN_LIBRARY_API_BASE_URL = "https://openlibrary.org/search.json"
    COST_PER_PAGE = 0.01

    def __init__(self):
        self.api_base_url = self.OPEN_LIBRARY_API_BASE_URL

    def search_book(self, title: str):
        """
        Searches for books with the given title on OpenLibrary.

        Args:
            title (str): The title of the book to search for.

        Returns:
            book_data (json): A dictionary containing the books of the search result
        """

        search_url = f"{self.api_base_url}?title={title}"
        response = requests.get(search_url)

        if response.status_code == HttpResponse.status_code:  # 200 OK
            # Step 2: Extract book details from the JSON response
            book_data = response.json()
            return book_data.get('docs', [])
        else:
            return []

    def rent_book(self, student_id, title, author, page_count, isbn, return_date):
        """
        Initiates a new book rental by fetching book details from OpenLibrary.

        Args:
            student_id (str): The student_id that wants to rent the book
            title (str): The title of the book to rent.
            author (str): The name of the author of the book
            page_count (int): The number of pages in the book.
            isbn (str): The ISBN of the book
            return_date (str): The date the student_id wants to return the book as a string
                in the format 'Month day, Year, Hour:Minute AM/PM'

        Returns:
            book (object): The rented book
        """
        # Create the rented book in the database
        book = Book(title=title, author=author, page_count=page_count, isbn=isbn)
        book.save()

        # Parse the return date string to a timezone-aware datetime object
        return_date_format = '%B %d, %Y, %I:%M %p'
        return_date = datetime.datetime.strptime(return_date, return_date_format)

        # Create the Rental object in the database
        rent = Rental(student_id_id=student_id, book_id=book, return_date=return_date)
        rent.save()

        # Calculate cost
        rented_date = rent.created  # Assuming rent.created represents the rented date
        rent_amount = self.calculate_rental_cost(number_of_pages=page_count, rented_date=rented_date,
                                                 return_date=return_date)

        # Save rental details
        self.save_rental_details(rent, rent_amount)

        return rent

    @staticmethod
    def calculate_rental_cost(number_of_pages, rented_date, return_date):
        """
        Calculates the rental cost based on the number of pages, rented date, and return date.

        Args:
            number_of_pages (int): The number of pages in the book.
            rented_date (datetime): The date the book was rented.
            return_date (datetime): The date the book was returned.

        Returns:
            float: The calculated rental cost.
        """
        # Example calculation: $0.01 per page, with the first month free
        cost_per_page = OpenLibraryBookRentalService.COST_PER_PAGE
        # Get the number of days in the current month
        current_month = rented_date.month
        days_in_month = calendar.monthrange(rented_date.year, current_month)[1]

        rented_date = rented_date.replace(tzinfo=None)

        return_date = return_date.replace(tzinfo=None)
        if return_date > rented_date + timedelta(days=days_in_month):
            # Calculate the rental cost only if the book is kept for more than a month
            return number_of_pages * cost_per_page
        else:
            return 0  # No cost if the book is returned within the first month

    @staticmethod
    def save_rental_details(rent, rental_cost):
        """
        Saves rental details in the system or database.

        Args:
            rent (Rent): The rent object
            rental_cost (float): The calculated rental cost.

        Returns:
            None
        """
        # Implement the logic to save rental details in your system/database
        rent.fee_amount = rental_cost
        rent.save()

    def rent_extension(self, rental_id, return_date):
        """
        Extend the return date of the rental.

        Args:
            rental_id (id): The rent object id
            return_date (Date): The new return date.

        Returns:
            None
        """
        return_date_format = '%Y-%m-%d'
        return_date = datetime.datetime.strptime(return_date, return_date_format)

        rental_object = Rental.objects.get(rental_id=rental_id)
        fee_amount = self.calculate_rental_cost(number_of_pages=rental_object.book_id.page_count,
                                                rented_date=rental_object.created, return_date=return_date)
        rental_object.fee_amount = fee_amount
        rental_object.return_date = return_date
        rental_object.save()
        return rental_object
