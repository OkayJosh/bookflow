import datetime

from django import forms


class BookSearchForm(forms.Form):
    search_query = forms.CharField(label='Search for a book', widget=forms.TextInput(attrs={'class': 'form-control'}))


class BookRentalForm(forms.Form):
    student_id = forms.CharField(label='Student ID', max_length=250)
    title = forms.CharField(label='Title', max_length=250)
    author = forms.CharField(label='Author', max_length=250)
    page_count = forms.IntegerField(label='Page Count', min_value=1, initial=100)
    isbn = forms.CharField(label='ISBN', max_length=13)
    return_date = forms.CharField(label='Return Date',
                                  initial=(datetime.datetime.today() + datetime.timedelta(days=30)))

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)  # Extract 'user_id' from kwargs
        super(BookRentalForm, self).__init__(*args, **kwargs)
        if user_id is not None:
            self.fields['student_id'] = forms.CharField(label='Student ID', max_length=10, initial=user_id)


class BookRentalExtensionForm(forms.Form):
    rental_id = forms.CharField(label='Student ID', max_length=250)
    return_date = forms.CharField(label='Return Date')


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=250)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
