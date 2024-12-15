from django.urls import path
# from .views import ShelfListView, ShelfCreateView, ShelfUpdateView, ShelfDeleteView, guest_view, book_list, \
#     BookListView, BookCreateView, BookUpdateView, BookDeleteView, AuthorListView, AuthorCreateView, AuthorUpdateView, \
#     AuthorDeleteView, GenreListView, GenreCreateView, GenreUpdateView, GenreDeleteView, HomeView, librarian_login
# from .views import register, login_view
# from .views import register, user_login
from .views import *


urlpatterns = [
    # path('register/', register, name='register'),
    # path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('liblogin/', librarian_login, name='login_lib'),

    path('shelves/', ShelfListView.as_view(), name='shelf_list'),
    path('shelves/add/', ShelfCreateView.as_view(), name='shelf_add'),
    path('shelves/edit/<int:pk>/', ShelfUpdateView.as_view(), name='shelf_edit'),
    path('shelves/delete/<int:pk>/', ShelfDeleteView.as_view(), name='shelf_delete'),

    path('books_1/', BookListView.as_view(), name='book_list_1'),
    path('books/add/', BookCreateView.as_view(), name='book_add'),
    path('books/edit/<int:pk>/', BookUpdateView.as_view(), name='book_edit'),
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),

    path('authors/', AuthorListView.as_view(), name='author_list'),
    path('authors/add/', AuthorCreateView.as_view(), name='author_add'),
    path('authors/edit/<int:pk>/', AuthorUpdateView.as_view(), name='author_edit'),
    path('authors/delete/<int:pk>/', AuthorDeleteView.as_view(), name='author_delete'),

    path('genres/', GenreListView.as_view(), name='genre_list'),
    path('genres/add/', GenreCreateView.as_view(), name='genre_add'),
    path('genres/edit/<int:pk>/', GenreUpdateView.as_view(), name='genre_edit'),
    path('genres/delete/<int:pk>/', GenreDeleteView.as_view(), name='genre_delete'),

    # path('admin/', admin_view, name='admin'),
    # path('librarian/', librarian_view, name='librarian'),
    # path('guest/', guest_view, name='guest'),

    path('guest/', guest_view, name='guest'),

    path('books/', book_list, name='book_list'),

    path('home_librarian', HomeView.as_view(), name='home'),
]
