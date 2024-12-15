from django import forms
from .models import Shelf, Reader, Book, Author, Genre
from django.contrib.auth.models import User

class ShelfForm(forms.ModelForm):
    class Meta:
        model = Shelf
        fields = ['location', 'capacity']

class ReaderRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# class ReaderRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Reader
#         fields = ['first_name', 'last_name', 'email', 'phone', 'username', 'password']
#         widgets = {
#             'password': forms.PasswordInput(),
#         }

class ReaderLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class ShelfForm(forms.ModelForm):
    class Meta:
        model = Shelf
        fields = ['location', 'capacity']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'genre']

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'birth_date', 'nationality']

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['genre_name']
