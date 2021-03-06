from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews, Profile, LogoProfile

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from modeltranslation.admin import TranslationAdmin


class MovieAdminForm(forms.ModelForm):
    """Форма с виджетом  ckeditor"""
    description_ru = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    """Категории"""
    list_display = ("id", "name", "url",)
    list_display_links = ("name",)
    prepopulated_fields = {'url': ('name',),}


class ReviewInline(admin.TabularInline):
    """Отзывы на страницы фильма"""
    model = Reviews
    extra = 1
    fields = ('name', 'text', 'parent','profile_user', 'email')
    # readonly_fields = ("name", "email")


class MovieShotsInline(admin.TabularInline):
    """Кадры из фильма на странице фильма"""
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image",)
    fields = ("title", "movie", "image")

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = "Изображения"


@admin.register(Movie)
class MovieAdmin(TranslationAdmin):
    """Фильмы"""
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    search_fields = ("title", "category__name")
    prepopulated_fields = {'url': ('title',), }
    inlines = [MovieShotsInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    form = MovieAdminForm
    actions = ["publish", "unpublish"]
    readonly_fields = ("get_image",)
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", ("poster", "get_image")),
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres", "category"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fees_in_world"),)
        }),
        (None, {
            "fields": (("url", "draft"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')

    get_image.short_description = "Постер"

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей было обновлено"
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей было обновлено"
        self.message_user(request, f'{message_bit}')

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change',)

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """ОТзывы к фильму"""
    list_display = ("name", "email", "parent", "movie", "id", 'profile_user')
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    """Жанры"""
    list_display = ("name", "url")


@admin.register(Actor)
class ActorAdmin(TranslationAdmin):
    """Актеры и режиссеры"""
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        try:
            return mark_safe(f'<img src={obj.image.url} width="50" height="60"')
        except:
            return ''

    get_image.short_description = "Изображения"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "movie", "ip")


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ("title", "movie", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображения"


admin.site.register(RatingStar)

admin.site.site_title = "Все о кино"
admin.site.site_header = "Все о кино"
admin.site.register(Profile)
admin.site.register(LogoProfile)
