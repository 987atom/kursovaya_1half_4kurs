from django.urls import path
from .views import ShelfListView, ShelfCreateView, ShelfUpdateView, ShelfDeleteView, guest_view, book_list, \
    BookListView, BookCreateView, BookUpdateView, BookDeleteView, AuthorListView, AuthorCreateView, AuthorUpdateView, \
    AuthorDeleteView, GenreListView, GenreCreateView, GenreUpdateView, GenreDeleteView, HomeView, librarian_login
# from .views import register, login_view
from .views import register, user_login


urlpatterns = [
    # path('register/', register, name='register'),
    # path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('liblogin/', librarian_login, name='login_lib'),

    path('shelves/', ShelfListView.as_view(), name='shelf_list'),  # Список полок
    path('shelves/add/', ShelfCreateView.as_view(), name='shelf_add'),  # Добавление полки
    path('shelves/edit/<int:pk>/', ShelfUpdateView.as_view(), name='shelf_edit'),  # Редактирование полки
    path('shelves/delete/<int:pk>/', ShelfDeleteView.as_view(), name='shelf_delete'),  # Удаление полки

    path('books_1/', BookListView.as_view(), name='book_list_1'),  # Список книг
    path('books/add/', BookCreateView.as_view(), name='book_add'),  # Добавление книги
    path('books/edit/<int:pk>/', BookUpdateView.as_view(), name='book_edit'),  # Редактирование книги
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),  # Удаление книги

    path('authors/', AuthorListView.as_view(), name='author_list'),  # Список авторов
    path('authors/add/', AuthorCreateView.as_view(), name='author_add'),  # Добавление автора
    path('authors/edit/<int:pk>/', AuthorUpdateView.as_view(), name='author_edit'),  # Редактирование автора
    path('authors/delete/<int:pk>/', AuthorDeleteView.as_view(), name='author_delete'),  # Удаление автора

    path('genres/', GenreListView.as_view(), name='genre_list'),  # Список жанров
    path('genres/add/', GenreCreateView.as_view(), name='genre_add'),  # Добавление жанра
    path('genres/edit/<int:pk>/', GenreUpdateView.as_view(), name='genre_edit'),  # Редактирование жанра
    path('genres/delete/<int:pk>/', GenreDeleteView.as_view(), name='genre_delete'),  # Удаление жанра

    # path('admin/', admin_view, name='admin'),
    # path('librarian/', librarian_view, name='librarian'),
    # path('guest/', guest_view, name='guest'),

    path('guest/', guest_view, name='guest'),

    path('books/', book_list, name='book_list'),

    path('home_librarian', HomeView.as_view(), name='home'),  # Главная страница

]
