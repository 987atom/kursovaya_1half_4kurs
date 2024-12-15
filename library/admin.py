import base64

from django.db import connection
from django.utils import timezone
from datetime import timedelta
from django.contrib import admin
from django.urls import path
from django.db.models import Count
import matplotlib.pyplot as plt
from io import BytesIO
import csv
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Author, Genre, Book, BookExemplar, Role, Reader, Staff, Shelf, Loan, BooksShelves


class AuthorAdmin(admin.ModelAdmin):
    # change_list_template = 'sale_summary_change_list.html'
    list_display = ('name', 'birth_date', 'nationality')
    search_fields = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('genre_name',)
    search_fields = ('genre_name',)


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'genre')
    search_fields = ('title',)
    list_filter = ('genre',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export/csv/', self.admin_site.admin_view(self.export_books_csv), name='export_books_csv'),
            path('import/csv/', self.admin_site.admin_view(self.import_books_csv), name='import_books_csv'),
            path('export/sql/', self.admin_site.admin_view(self.export_books_sql), name='export_books_sql'),
            path('import/sql/', self.admin_site.admin_view(self.import_books_sql), name='import_books_sql'),
            path('chart/<str:period>/', self.admin_site.admin_view(self.chart_view), name='book_chart'),
        ]
        return custom_urls + urls


    # def get_urls(self):
    #     urls = super().get_urls()
    #     custom_urls = [
    #         path('chart/<str:period>/', self.admin_site.admin_view(self.chart_view), name='book_chart'),
    #     ]
    #     return custom_urls + urls

    def export_books_csv(self, request):
        # Создаем HTTP-ответ с заголовками для CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="books.csv"'

        writer = csv.writer(response)
        writer.writerow(['Title', 'Author', 'Publication Year', 'Genre'])  # Заголовки столбцов

        for book in Book.objects.all():
            writer.writerow([book.title, book.author.name, book.publication_year, book.genre.genre_name])

        return response

    def import_books_csv(self, request):
        # Обработка загрузки файла
        if request.method == 'POST' and request.FILES['file']:
            file = request.FILES['file']
            reader = csv.reader(file.read().decode('utf-8').splitlines())
            next(reader)  # Пропускаем заголовок

            for row in reader:
                author, _ = Author.objects.get_or_create(
                    name=row[1])  # Предполагается, что автор уже существует или будет создан
                genre, _ = Genre.objects.get_or_create(
                    genre_name=row[3])  # Предполагается, что жанр уже существует или будет создан
                Book.objects.create(
                    title=row[0],
                    author=author,
                    publication_year=row[2],
                    genre=genre
                )
            return redirect('admin:library_book_changelist')  # Замените 'yourappname' на имя вашего приложения

        return render(request, 'import_books.html')

    def export_books_sql(self, request):
        # Создаем HTTP-ответ с заголовками для SQL
        response = HttpResponse(content_type='text/sql')
        response['Content-Disposition'] = 'attachment; filename="books.sql"'

        # Начинаем формировать SQL-скрипт
        sql_script = ""

        # Получаем все книги и формируем SQL-запросы
        books = Book.objects.all()  # Получаем все книги из базы данных
        for book in books:
            sql_script += f"INSERT INTO library_book (title, author_id, publication_year, genre_id) VALUES ('{book.title}', {book.author.id}, {book.publication_year}, {book.genre.id});\n"

        # Записываем скрипт в ответ
        response.write(sql_script)

        return response

    def import_books_sql(self, request):
        if request.method == 'POST' and request.FILES['file']:
            file = request.FILES['file']

            # Считываем SQL-скрипт из загруженного файла
            sql_script = file.read().decode('utf-8')
            sql_statements = sql_script.split(';')  # Разделяем на отдельные запросы

            with connection.cursor() as cursor:
                for statement in sql_statements:
                    statement = statement.strip()
                    if statement:  # Проверяем, что запрос не пустой
                        try:
                            cursor.execute(statement)  # Выполняем каждый запрос отдельно
                        except Exception as e:
                            return HttpResponse(f"Ошибка при выполнении запроса: {str(e)}")

            return HttpResponse("Данные успешно импортированы.")

        return render(request, 'import_books_sql.html')

    def chart_view(self, request, period):
        # Получаем текущую дату
        now = timezone.now()

        # Определяем начальную дату в зависимости от выбранного периода
        if period == 'day':
            start_date = now - timedelta(days=1)
        elif period == 'month':
            start_date = now - timedelta(days=30)
        elif period == 'year':
            start_date = now - timedelta(days=365)
        else:  # 'all'
            start_date = None  # Для всех данных

        # Получаем данные о количестве книг по жанрам
        if start_date:
            genre_data = Genre.objects.annotate(book_count=Count('book')).filter(
                book__publication_year__gte=start_date.year)
        else:
            genre_data = Genre.objects.annotate(book_count=Count('book'))

        # Генерация графика
        genres = [g.genre_name for g in genre_data]
        counts = [g.book_count for g in genre_data]

        plt.figure(figsize=(10, 6))
        plt.bar(genres, counts, color='skyblue')
        plt.xlabel('Жанр')
        plt.ylabel('Количество книг')
        plt.title(f'Количество книг по жанрам за период: {period}')
        plt.xticks(rotation=45)

        # Сохранение графика в буфер
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        # Кодирование изображения в Base64
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')

        return render(request, "admin/book_chart.html", {'image_file': image_base64, 'period': period})


class BookExemplarAdmin(admin.ModelAdmin):
    list_display = ('book', 'print_date', 'condition')
    list_filter = ('book',)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name',)
    search_fields = ('role_name',)


class ReaderAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'role')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('role',)


class StaffAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'position', 'role')
    search_fields = ('first_name', 'last_name', 'position')
    list_filter = ('role',)


class ShelfAdmin(admin.ModelAdmin):
    list_display = ('location', 'capacity')
    search_fields = ('location',)


class LoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'reader', 'loan_date', 'return_date', 'is_returned')
    list_filter = ('is_returned', 'loan_date')
    search_fields = ('book__title', 'reader__username')


class BooksShelvesAdmin(admin.ModelAdmin):
    list_display = ('book', 'shelf')
    list_filter = ('shelf',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookExemplar, BookExemplarAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Reader, ReaderAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Shelf, ShelfAdmin)
admin.site.register(Loan, LoanAdmin)
admin.site.register(BooksShelves, BooksShelvesAdmin)
