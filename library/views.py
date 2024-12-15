import csv
import logging

import pandas as pd
from django.views import View

from django.utils import timezone
from .utils import authenticate_reader
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Shelf
from .forms import ShelfForm, BookForm, AuthorForm, GenreForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, login
from .forms import ReaderRegistrationForm, ReaderLoginForm
from .models import Reader
from django.contrib.auth.decorators import login_required, user_passes_test

def book_list(request):
    books = Book.objects.all()  # Извлекаем все книги
    return render(request, 'books/book_list.html', {'books': books})



def is_admin(user):
    return user.groups.filter(name='Администратор').exists()

def is_librarian(user):
    return user.groups.filter(name='Библиотекарь').exists()

@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'admin.html')

@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'librarian.html')

@login_required
def guest_view(request):
    return render(request, 'guest.html')



@method_decorator(login_required, name='dispatch')
class ShelfListView(ListView):
    model = Shelf
    template_name = 'shelf_list.html'

    def get_queryset(self):
        # Проверка роли пользователя
        if self.request.user.role.role_name == 'Обычный сотрудник':
            return super().get_queryset()
        else:
            return Shelf.objects.none()  # Возвращаем пустой queryset

@method_decorator(login_required, name='dispatch')
class ShelfCreateView(CreateView):
    model = Shelf
    form_class = ShelfForm
    template_name = 'shelf_form.html'
    success_url = reverse_lazy('shelf_list')

    def form_valid(self, form):
        capacity = form.cleaned_data.get('capacity')
        if capacity < 0:
            form.add_error('capacity', 'Вместимость полки не может быть отрицательной.')
            return self.form_invalid(form)
        return super().form_valid(form)

    # def form_valid(self, form):
    #     if self.request.user.role.role_name == 'Обычный сотрудник':
    #         return super().form_valid(form)
    #     return redirect('shelf_list')

@method_decorator(login_required, name='dispatch')
class ShelfUpdateView(UpdateView):
    model = Shelf
    form_class = ShelfForm
    template_name = 'shelf_form.html'
    success_url = reverse_lazy('shelf_list')

    def form_valid(self, form):
        capacity = form.cleaned_data.get('capacity')
        if capacity < 0:
            form.add_error('capacity', 'Вместимость полки не может быть отрицательной.')
            return self.form_invalid(form)
        return super().form_valid(form)

    # def form_valid(self, form):
    #     if self.request.user.role.role_name == 'Обычный сотрудник':
    #         return super().form_valid(form)
    #     return redirect('shelf_list')

@method_decorator(login_required, name='dispatch')
class ShelfDeleteView(DeleteView):
    model = Shelf
    template_name = 'shelf_confirm_delete.html'
    success_url = reverse_lazy('shelf_list')

    def get_queryset(self):
        if self.request.user.role.role_name == 'Обычный сотрудник':
            return super().get_queryset()
        return Shelf.objects.none()


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.groups.filter(name='Администратор').exists():
                return redirect('admin')
            elif user.groups.filter(name='Библиотекарь').exists():
                return redirect('librarian')
            else:
                return redirect('book_list')
    return render(request, 'login.html')

def librarian_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.groups.filter(name='Администратор').exists():
                return redirect('admin')
            elif user.groups.filter(name='Библиотекарь').exists():
                return redirect('librarian')
            else:
                return redirect('home')
    return render(request, 'login.html')

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             if user.groups.filter(name='Администратор').exists():
#                 return redirect('admin')
#             elif user.groups.filter(name='Библиотекарь').exists():
#                 return redirect('librarian')
#             else:
#                 return redirect('guest')
#     return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = ReaderRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Добавляем пользователя в группу "Гость" по умолчанию
            guest_group = Group.objects.get(name='Гость')
            guest_group.user_set.add(user)

            return redirect('login')
    else:
        form = ReaderRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

# def register(request):
#     if request.method == 'POST':
#         form = ReaderRegistrationForm(request.POST)
#         if form.is_valid():
#             reader = form.save(commit=False)
#             guest_role = Role.objects.get(role_name='гость')
#             reader.role = guest_role  # Присваиваем роль
#             reader.save()  # Сохраняем пароль в открытом виде
#             return redirect('login')
#     else:
#         form = ReaderRegistrationForm()
#     return render(request, 'registration/register.html', {'form': form})
#
#
#
# def login_view(request):
#     if request.method == 'POST':
#         form = ReaderLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username'].strip()  # Удаляем пробелы
#             password = form.cleaned_data['password'].strip()
#             user = authenticate_reader(username, password)
#             if user is not None:
#                 auth_login(request, user)
#                 return redirect('home')
#             else:
#                 return render(request, 'registration/login.html', {'form': form, 'error': 'Неверное имя пользователя или пароль.'})
#     else:
#         form = ReaderLoginForm()
#     return render(request, 'registration/login.html', {'form': form})





def export_books_csv(request):
    # Создаем HTTP-ответ с заголовками для CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="books.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Author', 'Publication Year', 'Genre'])  # Заголовки столбцов

    for book in Book.objects.all():
        writer.writerow([book.title, book.author.name, book.publication_year, book.genre.genre_name])

    return response

def import_books_csv(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        df = pd.read_csv(file)

        for index, row in df.iterrows():
            # Предполагаем, что в CSV есть колонки: Title, Author, Publication Year, Genre
            author, created = Author.objects.get_or_create(name=row['Author'])
            genre, created = Genre.objects.get_or_create(genre_name=row['Genre'])
            Book.objects.create(
                title=row['Title'],
                author=author,
                publication_year=row['Publication Year'],
                genre=genre
            )
        return render(request, 'import_success.html')

    return render(request, 'import_books.html')

class ShelfListView(View):
    def get(self, request):
        shelves = Shelf.objects.all()
        return render(request, 'shelves/shelf_list.html', {'shelves': shelves})

class ShelfCreateView(View):
    def get(self, request):
        form = ShelfForm()
        return render(request, 'shelves/shelf_form.html', {'form': form})

    def post(self, request):
        form = ShelfForm(request.POST)
        if form.is_valid():
            capacity = form.cleaned_data.get('capacity')
            if capacity < 1:  # Проверка на отрицательную вместимость
                form.add_error('capacity', 'Вместимость полки не может быть ниже 0.')
                return render(request, 'shelves/shelf_form.html', {'form': form})
            form.save()
            return redirect('shelf_list')  # Перенаправление на список полок
        return render(request, 'shelves/shelf_form.html', {'form': form})

    # def post(self, request):
    #     form = ShelfForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('shelf_list')  # Перенаправление на список полок
    #     return render(request, 'shelves/shelf_form.html', {'form': form})

class ShelfUpdateView(View):
    def get(self, request, pk):
        shelf = get_object_or_404(Shelf, pk=pk)
        form = ShelfForm(instance=shelf)
        return render(request, 'shelves/shelf_form.html', {'form': form})

    # def post(self, request):
    #     form = ShelfForm(request.POST)
    #     if form.is_valid():
    #         capacity = form.cleaned_data.get('capacity')
    #         if capacity < 1:  # Проверка на отрицательную вместимость
    #             form.add_error('capacity', 'Вместимость полки не может быть ниже 0.')
    #             return render(request, 'shelves/shelf_form.html', {'form': form})
    #         form.save()
    #         return redirect('shelf_list')  # Перенаправление на список полок
    #     return render(request, 'shelves/shelf_form.html', {'form': form})

    def post(self, request, pk):
        shelf = get_object_or_404(Shelf, pk=pk)
        form = ShelfForm(request.POST, instance=shelf)
        if form.is_valid():
            capacity = form.cleaned_data.get('capacity')
            if capacity < 1:  # Проверка на отрицательную вместимость
                form.add_error('capacity', 'Вместимость полки не может быть ниже 0.')
                return render(request, 'shelves/shelf_form.html', {'form': form})
            form.save()
            return redirect('shelf_list')
        return render(request, 'shelves/shelf_form.html', {'form': form})

class ShelfDeleteView(View):
    def get(self, request, pk):
        shelf = get_object_or_404(Shelf, pk=pk)
        return render(request, 'shelves/shelf_confirm_delete.html', {'shelf': shelf})

    def post(self, request, pk):
        shelf = get_object_or_404(Shelf, pk=pk)
        shelf.delete()
        return redirect('shelf_list')

class BookListView(View):
    def get(self, request):
        books = Book.objects.all()  # Получаем все книги
        return render(request, 'books/book_list_1.html', {'books': books})

class BookCreateView(View):
    def get(self, request):
        form = BookForm()
        return render(request, 'books/book_form.html', {'form': form})

    def post(self, request):
        form = BookForm(request.POST)
        if form.is_valid():
            publication_year = form.cleaned_data.get('publication_year')
            current_year = timezone.now().year
            # if publication_year > current_year:
            #     form.add_error('publication_year', 'Год издания не может быть в будущем.')
            #     return render(request, 'books/book_form.html', {'form': form})
            # Проверка на год издания
            if publication_year < 0:
                form.add_error('publication_year', 'Год издания не может быть меньше нуля.')
                return render(request, 'books/book_form.html', {'form': form})
            if publication_year > current_year:
                form.add_error('publication_year', 'Год издания не может быть в будущем.')
                return render(request, 'books/book_form.html', {'form': form})
            form.save()
            return redirect('book_list_1')
        return render(request, 'books/book_form.html', {'form': form})

    # def post(self, request):
    #     form = BookForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('book_list_1')  # Перенаправление на список книг
    #     return render(request, 'books/book_form.html', {'form': form})

class BookUpdateView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = BookForm(instance=book)
        return render(request, 'books/book_form.html', {'form': form})

    # def post(self, request, pk):
    #     book = get_object_or_404(Book, pk=pk)
    #     form = BookForm(request.POST, instance=book)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('book_list_1')
    #     return render(request, 'books/book_form.html', {'form': form})

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            publication_year = form.cleaned_data.get('publication_year')
            current_year = timezone.now().year
            # Проверка на год издания
            if publication_year < 0:
                form.add_error('publication_year', 'Год издания не может быть меньше нуля.')
                return render(request, 'books/book_form.html', {'form': form})
            if publication_year > current_year:
                form.add_error('publication_year', 'Год издания не может быть в будущем.')
                return render(request, 'books/book_form.html', {'form': form})
            form.save()
            return redirect('book_list_1')
        return render(request, 'books/book_form.html', {'form': form})

class BookDeleteView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return render(request, 'books/book_confirm_delete.html', {'book': book})

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return redirect('book_list_1')\

class AuthorListView(View):
    def get(self, request):
        authors = Author.objects.all()  # Получаем всех авторов
        return render(request, 'authors/author_list.html', {'authors': authors})

class AuthorCreateView(View):
    def get(self, request):
        form = AuthorForm()
        return render(request, 'authors/author_form.html', {'form': form})

    def post(self, request):
        form = AuthorForm(request.POST)
        if form.is_valid():
            birth_date = form.cleaned_data.get('birth_date')
            if birth_date and birth_date > timezone.now().date():
                form.add_error('birth_date', "Дата рождения не может быть в будущем.")
            else:
                form.save()
                return redirect('author_list')  # Перенаправление на список авторов
        return render(request, 'authors/author_form.html', {'form': form})

    # def post(self, request):
    #     form = AuthorForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('author_list')  # Перенаправление на список авторов
    #     return render(request, 'authors/author_form.html', {'form': form})

class AuthorUpdateView(View):
    def get(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        form = AuthorForm(instance=author)
        return render(request, 'authors/author_form.html', {'form': form})

    def post(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            birth_date = form.cleaned_data.get('birth_date')
            if birth_date and birth_date > timezone.now().date():
                form.add_error('birth_date', "Дата рождения не может быть в будущем.")
            else:
                form.save()
                return redirect('author_list')  # Перенаправление на список авторов
            return redirect('author_list')
        return render(request, 'authors/author_form.html', {'form': form})

class AuthorDeleteView(View):
    def get(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        return render(request, 'authors/author_confirm_delete.html', {'author': author})

    def post(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        author.delete()
        return redirect('author_list')

class GenreListView(View):
    def get(self, request):
        genres = Genre.objects.all()  # Получаем все жанры
        return render(request, 'genres/genre_list.html', {'genres': genres})

class GenreCreateView(View):
    def get(self, request):
        form = GenreForm()
        return render(request, 'genres/genre_form.html', {'form': form})

    def post(self, request):
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('genre_list')  # Перенаправление на список жанров
        return render(request, 'genres/genre_form.html', {'form': form})

class GenreUpdateView(View):
    def get(self, request, pk):
        genre = get_object_or_404(Genre, pk=pk)
        form = GenreForm(instance=genre)
        return render(request, 'genres/genre_form.html', {'form': form})

    def post(self, request, pk):
        genre = get_object_or_404(Genre, pk=pk)
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            form.save()
            return redirect('genre_list')
        return render(request, 'genres/genre_form.html', {'form': form})

class GenreDeleteView(View):
    def get(self, request, pk):
        genre = get_object_or_404(Genre, pk=pk)
        return render(request, 'genres/genre_confirm_delete.html', {'genre': genre})

    def post(self, request, pk):
        genre = get_object_or_404(Genre, pk=pk)
        genre.delete()
        return redirect('genre_list')

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')
