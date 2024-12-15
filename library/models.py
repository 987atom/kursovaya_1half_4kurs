from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group


def assign_permissions():
    admin_group = Group.objects.get(name='Администратор')
    librarian_group = Group.objects.get(name='Библиотекарь')

    # Пример прав
    permissions = {
        'can_add_book': 'Добавление книги',
        'can_edit_book': 'Редактирование книги',
        'can_view_books': 'Просмотр книг',
    }

    for codename, name in permissions.items():
        permission, created = Permission.objects.get_or_create(codename=codename, name=name)
        admin_group.permissions.add(permission)  # Администратор получает все права
        librarian_group.permissions.add(permission)  # Библиотекарь получает права на просмотр и редактирование

class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Имя"))
    birth_date = models.DateField(null=True, blank=True, verbose_name=_("Дата рождения"))
    nationality = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Национальность"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Автор")
        verbose_name_plural = _("Авторы")


class Genre(models.Model):
    genre_name = models.CharField(max_length=100, verbose_name=_("Жанр"))

    def __str__(self):
        return self.genre_name

    class Meta:
        verbose_name = _("Жанр")
        verbose_name_plural = _("Жанры")


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Название"))
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_("Автор"))
    publication_year = models.IntegerField(verbose_name=_("Год публикации"))
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name=_("Жанр"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Книга")
        verbose_name_plural = _("Книги")


class BookExemplar(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_("Книга"))
    print_date = models.DateField(verbose_name=_("Дата печати"))
    condition = models.CharField(max_length=100, verbose_name=_("Состояние"))

    class Meta:
        unique_together = ('book', 'id')
        verbose_name = _("Экземпляр книги")
        verbose_name_plural = _("Экземпляры книг")

    def __str__(self):
        return f"{self.book.title} (Экземпляр {self.id})"


class Role(models.Model):
    role_name = models.CharField(max_length=100, verbose_name=_("Название роли"))

    def __str__(self):
        return self.role_name

    class Meta:
        verbose_name = _("Роль")
        verbose_name_plural = _("Роли")


# class Reader(models.Model):
#     first_name = models.CharField(max_length=100, verbose_name=_("Имя"))
#     last_name = models.CharField(max_length=100, verbose_name=_("Фамилия"))
#     email = models.EmailField(unique=True, verbose_name=_("Электронная почта"))
#     phone = models.CharField(max_length=15, null=True, blank=True, verbose_name=_("Телефон"))
#     username = models.CharField(max_length=100, unique=True, verbose_name=_("Имя пользователя"))
#     password = models.CharField(max_length=255, verbose_name=_("Пароль"))
#     role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name=_("Роль"))
#
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"
#
#     class Meta:
#         verbose_name = _("Читатель")
#         verbose_name_plural = _("Читатели")

class Reader(models.Model):
    first_name = models.CharField(max_length=100, verbose_name=_("Имя"))
    last_name = models.CharField(max_length=100, verbose_name=_("Фамилия"))
    email = models.EmailField(unique=True, verbose_name=_("Электронная почта"))
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name=_("Телефон"))
    username = models.CharField(max_length=100, unique=True, verbose_name=_("Имя пользователя"))
    password = models.CharField(max_length=255, verbose_name=_("Пароль"))  # Оставляем без изменений
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name=_("Роль"))
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _("Читатель")
        verbose_name_plural = _("Читатели")




class Staff(models.Model):
    first_name = models.CharField(max_length=100, verbose_name=_("Имя"))
    last_name = models.CharField(max_length=100, verbose_name=_("Фамилия"))
    position = models.CharField(max_length=100, verbose_name=_("Должность"))
    username = models.CharField(max_length=100, unique=True, verbose_name=_("Имя пользователя"))
    password = models.CharField(max_length=255, verbose_name=_("Пароль"))
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name=_("Роль"))

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"

    class Meta:
        verbose_name = _("Сотрудник")
        verbose_name_plural = _("Сотрудники")


class Shelf(models.Model):
    location = models.CharField(max_length=255, verbose_name=_("Место нахождения"))
    capacity = models.IntegerField(verbose_name=_("Вместимость"))

    def __str__(self):
        return self.location

    class Meta:
        verbose_name = _("Полка")
        verbose_name_plural = _("Полки")


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_("Книга"))
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name=_("Читатель"))
    loan_date = models.DateField(verbose_name=_("Дата займа"))
    return_date = models.DateField(null=True, blank=True, verbose_name=_("Дата возврата"))
    is_returned = models.BooleanField(default=False, verbose_name=_("Возвращено?"))

    def __str__(self):
        return f"Заем {self.book.title} читателю {self.reader.username}"

    class Meta:
        verbose_name = _("Заем")
        verbose_name_plural = _("Заемы")


class BooksShelves(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_("Книга"))
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE, verbose_name=_("Полка"))

    def __str__(self):
        return f"{self.book.title} на полке {self.shelf.location}"

    class Meta:
        verbose_name = _("Книга на полке")
        verbose_name_plural = _("Книги на полках")
