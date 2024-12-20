# Generated by Django 5.1.2 on 2024-11-29 11:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'verbose_name': 'Автор', 'verbose_name_plural': 'Авторы'},
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'verbose_name': 'Книга', 'verbose_name_plural': 'Книги'},
        ),
        migrations.AlterModelOptions(
            name='bookexemplar',
            options={'verbose_name': 'Экземпляр книги', 'verbose_name_plural': 'Экземпляры книг'},
        ),
        migrations.AlterModelOptions(
            name='booksshelves',
            options={'verbose_name': 'Книга на полке', 'verbose_name_plural': 'Книги на полках'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'verbose_name': 'Жанр', 'verbose_name_plural': 'Жанры'},
        ),
        migrations.AlterModelOptions(
            name='loan',
            options={'verbose_name': 'Заем', 'verbose_name_plural': 'Заемы'},
        ),
        migrations.AlterModelOptions(
            name='reader',
            options={'verbose_name': 'Читатель', 'verbose_name_plural': 'Читатели'},
        ),
        migrations.AlterModelOptions(
            name='role',
            options={'verbose_name': 'Роль', 'verbose_name_plural': 'Роли'},
        ),
        migrations.AlterModelOptions(
            name='shelf',
            options={'verbose_name': 'Полка', 'verbose_name_plural': 'Полки'},
        ),
        migrations.AlterModelOptions(
            name='staff',
            options={'verbose_name': 'Сотрудник', 'verbose_name_plural': 'Сотрудники'},
        ),
        migrations.AlterField(
            model_name='author',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='author',
            name='nationality',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Национальность'),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.author', verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.genre', verbose_name='Жанр'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publication_year',
            field=models.IntegerField(verbose_name='Год публикации'),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='bookexemplar',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.book', verbose_name='Книга'),
        ),
        migrations.AlterField(
            model_name='bookexemplar',
            name='condition',
            field=models.CharField(max_length=100, verbose_name='Состояние'),
        ),
        migrations.AlterField(
            model_name='bookexemplar',
            name='print_date',
            field=models.DateField(verbose_name='Дата печати'),
        ),
        migrations.AlterField(
            model_name='booksshelves',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.book', verbose_name='Книга'),
        ),
        migrations.AlterField(
            model_name='booksshelves',
            name='shelf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.shelf', verbose_name='Полка'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='genre_name',
            field=models.CharField(max_length=100, verbose_name='Жанр'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.book', verbose_name='Книга'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='is_returned',
            field=models.BooleanField(default=False, verbose_name='Возвращено?'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='loan_date',
            field=models.DateField(verbose_name='Дата займа'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='reader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.reader', verbose_name='Читатель'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='return_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата возврата'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Электронная почта'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='password',
            field=models.CharField(max_length=255, verbose_name='Пароль'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.role', verbose_name='Роль'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='username',
            field=models.CharField(max_length=100, unique=True, verbose_name='Имя пользователя'),
        ),
        migrations.AlterField(
            model_name='role',
            name='role_name',
            field=models.CharField(max_length=100, verbose_name='Название роли'),
        ),
        migrations.AlterField(
            model_name='shelf',
            name='capacity',
            field=models.IntegerField(verbose_name='Вместимость'),
        ),
        migrations.AlterField(
            model_name='shelf',
            name='location',
            field=models.CharField(max_length=255, verbose_name='Место нахождения'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='password',
            field=models.CharField(max_length=255, verbose_name='Пароль'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='position',
            field=models.CharField(max_length=100, verbose_name='Должность'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.role', verbose_name='Роль'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='username',
            field=models.CharField(max_length=100, unique=True, verbose_name='Имя пользователя'),
        ),
    ]
