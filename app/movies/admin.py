from django.contrib import admin
from .models import Genre, FilmWork, Person, GenreFilmWork, PersonFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = (
        'name',
        'description',
        'created',
        'modified'
    )


    # Поиск по полям
    search_fields = ('name', 'description', 'id')
    pass


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline,)
    # Отображение полей в списке
    list_display = ('title', 'type', 'creation_date', 'rating', 'created', 'modified')
    # Фильтрация в списке
    list_filter = ('type', 'rating', 'creation_date')
    # Поиск по полям
    search_fields = ('title', 'description', 'id')

    list_prefetch_related = ('persons', 'genres')

    def get_queryset(self, request):
        queryset = (
            super().get_queryset(request).prefetch_related(
                *self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ','.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = 'Жанры фильма'


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmWorkInline,)
    list_display = ('full_name', 'created', 'modified')
    search_fields = ('full_name', 'id')
