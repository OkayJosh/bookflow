import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from rental.models import Rental
from services.book_rental_service import OpenLibraryBookRentalService
from rental.forms import BookSearchForm, BookRentalForm, LoginForm, BookRentalExtensionForm
from student.models import Student


class LoginView(View):
    """
    Class-based view for user login.
    """
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('book_search')  # Redirect to the home page after login
            else:
                # Add an error message for invalid credentials
                form.add_error(None, 'Invalid username or password.')
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    """
    Class-based view for user logout.
    """

    def get(self, request):
        logout(request)
        return redirect('login')  # Redirect to the login page after logout


class BookSearchView(View):
    """
    Class-based view for book searching.
    """
    template_name = 'book_search.html'

    @method_decorator(login_required)
    def get(self, request):
        search_form = BookSearchForm()
        rented_books = self.get_rented_books(request.user)
        return render(request, self.template_name,
                      {'search_form': search_form,
                       'search_results': [],
                       'rented_books': rented_books,
                       'user': request.user.student_id})

    @method_decorator(login_required)
    def post(self, request):
        search_form = BookSearchForm(request.POST)
        rented_books = self.get_rented_books(request.user)
        default_return_date = datetime.datetime.today() + datetime.timedelta(days=30)
        if search_form.is_valid():
            search_query = search_form.cleaned_data['search_query']
            book_search = OpenLibraryBookRentalService()
            book_search_result = book_search.search_book(search_query)
            return render(request, self.template_name,
                          {'search_form': search_form,
                           'search_results': book_search_result,
                           'rented_books': rented_books,
                           'user': request.user.student_id,
                           'default_return_date': default_return_date.strftime('%B %d, %Y, %I:%M %p')})
        return render(request, self.template_name,
                      {'search_form': search_form,
                       'search_results': [],
                       'rented_books': rented_books,
                       'user': request.user.student_id,
                       'default_return_date': default_return_date})

    def get_rented_books(self, user):
        """
        Helper method to get the books rented by the user.

        Args:
            user: The user object.

        Returns:
            Rental Object.
        """
        # Implement logic to fetch rented books for the user from the database or any other source

        return Rental.objects.select_related('book_id').filter(student_id=user).order_by('-created')


class BookRentView(View):
    """
    Class-based view for book rental.
    """
    template_name = 'book_rent.html'

    @method_decorator(login_required)
    def get(self, request):
        rent_form = BookRentalForm()
        return render(request, self.template_name, {'book_rented': None, 'rent_form': rent_form})

    @method_decorator(login_required)
    def post(self, request):
        rent_form = BookRentalForm(request.POST)
        if rent_form.is_valid():
            book_service = OpenLibraryBookRentalService()
            book_rented = book_service.rent_book(**rent_form.cleaned_data)
            return render(request, self.template_name, {'book_rented': book_rented, 'rent_form': rent_form})
        return render(request, self.template_name, {'book_rented': None, 'rent_form': rent_form})


class BookRentExtensionView(View):
    """
    Class-based view for book rental.
    """
    template_name = 'book_rent_extension.html'

    @method_decorator(login_required)
    def get(self, request):
        extension_form = BookRentalExtensionForm()
        return render(request, self.template_name, {'book_rented': None, 'extension_form': extension_form})

    @method_decorator(login_required)
    def post(self, request):
        extension_form = BookRentalExtensionForm(request.POST)
        if extension_form.is_valid():
            book_service = OpenLibraryBookRentalService()
            book_rented = book_service.rent_extension(**extension_form.cleaned_data)
            return render(request, self.template_name, {'book_rented': book_rented, 'rent_form': extension_form})
        return render(request, self.template_name, {'book_rented': None, 'rent_form': extension_form})


class StudentListView(View):
    """
    Admin view to display a list of students and their borrowed books.
    """
    template_name = 'admin/list_students.html'

    @method_decorator(staff_member_required(login_url='login'))
    def get(self, request):
        students = Student.objects.all()

        return render(request, self.template_name, {'students': students})


class BorrowedBooksView(View):
    """
    Admin view to display borrowed books for a specific student.
    """
    template_name = 'admin/borrowed_books.html'

    @method_decorator(staff_member_required(login_url='login'))
    def get(self, request, student_id):
        search_form = BookSearchForm()
        rented_books = self.get_rented_books(student_id)

        # return render(request, self.template_name, {'student': student, 'rented_books': rented_books})

        return render(request, self.template_name,
                      {'search_form': search_form,
                       'search_results': [],
                       'rented_books': rented_books,
                       'user': student_id})

    @method_decorator(staff_member_required(login_url='login'))
    def post(self, request, student_id):
        search_form = BookSearchForm(request.POST)
        rented_books = self.get_rented_books(student_id)
        default_return_date = datetime.datetime.today() + datetime.timedelta(days=30)
        if search_form.is_valid():
            search_query = search_form.cleaned_data['search_query']
            book_search = OpenLibraryBookRentalService()
            book_search_result = book_search.search_book(search_query)
            return render(request, self.template_name,
                          {'search_form': search_form,
                           'search_results': book_search_result,
                           'rented_books': rented_books,
                           'user': student_id,
                           'default_return_date': default_return_date.strftime('%B %d, %Y, %I:%M %p')})
        return render(request, self.template_name,
                      {'search_form': search_form,
                       'search_results': [],
                       'rented_books': rented_books,
                       'user': student_id,
                       'default_return_date': default_return_date})

    def get_rented_books(self, student_id):
        """
        Helper method to get the books rented by the user.

        Args:
            user: The user object.

        Returns:
            Rental Object.
        """
        # Implement logic to fetch rented books for the user from the database or any other source

        return Rental.objects.select_related('book_id').filter(student_id_id=student_id).order_by('-created')