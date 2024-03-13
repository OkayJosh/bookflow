from django.urls import path

from rental.views import LoginView, LogoutView, BookSearchView, BookRentView, BookRentExtensionView, BorrowedBooksView, \
    StudentListView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('', LogoutView.as_view(), name='logout'),
    path('book-search/', BookSearchView.as_view(), name='book_search'),
    path('book-rent/', BookRentView.as_view(), name='book_rent'),
    path('book-rent-extension/', BookRentExtensionView.as_view(), name='book_rent_extension'),
    #Admin
    path('admin/list-students/', StudentListView.as_view(), name='admin_list_students'),
    path('admin/borrowed-books/<uuid:student_id>/', BorrowedBooksView.as_view(), name='admin_borrowed_books'),
]
